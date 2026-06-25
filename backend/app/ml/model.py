"""
VatteluttuX - CNN Model Architecture

A ResNet-inspired CNN for single character classification.
Input: 1x64x64 grayscale image
Output: num_classes probabilities
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvBlock(nn.Module):
    """Convolutional block with BatchNorm and ReLU."""
    
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 3, stride: int = 1, padding: int = 1):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, bias=False)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
    
    def forward(self, x):
        return self.relu(self.bn(self.conv(x)))


class ResidualBlock(nn.Module):
    """Residual block with skip connection."""
    
    def __init__(self, channels: int):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, 1, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, 1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU(inplace=True)
    
    def forward(self, x):
        residual = x
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual
        return self.relu(out)


class VatteluttuCNN(nn.Module):
    """
    CNN classifier for Vatteluttu character recognition.
    
    Architecture:
    - Initial conv block: 1 -> 32 channels
    - 4 stages with increasing channels (32 -> 64 -> 128 -> 256)
    - Each stage has conv + residual block + max pool
    - Global average pooling
    - Fully connected classifier
    
    Input: (batch, 1, 64, 64)
    Output: (batch, num_classes)
    """
    
    def __init__(self, num_classes: int = 247, dropout: float = 0.5):
        super().__init__()
        
        self.num_classes = num_classes
        
        # Initial convolution
        self.initial = ConvBlock(1, 32, kernel_size=3, stride=1, padding=1)
        
        # Stage 1: 32 -> 64 channels, 64x64 -> 32x32
        self.stage1 = nn.Sequential(
            ConvBlock(32, 64, kernel_size=3, stride=1, padding=1),
            ResidualBlock(64),
            nn.MaxPool2d(2, 2)
        )
        
        # Stage 2: 64 -> 128 channels, 32x32 -> 16x16
        self.stage2 = nn.Sequential(
            ConvBlock(64, 128, kernel_size=3, stride=1, padding=1),
            ResidualBlock(128),
            nn.MaxPool2d(2, 2)
        )
        
        # Stage 3: 128 -> 256 channels, 16x16 -> 8x8
        self.stage3 = nn.Sequential(
            ConvBlock(128, 256, kernel_size=3, stride=1, padding=1),
            ResidualBlock(256),
            nn.MaxPool2d(2, 2)
        )
        
        # Stage 4: 256 -> 512 channels, 8x8 -> 4x4
        self.stage4 = nn.Sequential(
            ConvBlock(256, 512, kernel_size=3, stride=1, padding=1),
            ResidualBlock(512),
            nn.MaxPool2d(2, 2)
        )
        
        # Global average pooling
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        
        # Classifier
        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout * 0.5),
            nn.Linear(256, num_classes)
        )
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Initialize weights using He initialization."""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
    
    def forward(self, x):
        """Forward pass."""
        x = self.initial(x)
        x = self.stage1(x)
        x = self.stage2(x)
        x = self.stage3(x)
        x = self.stage4(x)
        x = self.global_pool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x
    
    def predict(self, x):
        """Get predictions with probabilities."""
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            probs = F.softmax(logits, dim=1)
            preds = torch.argmax(probs, dim=1)
        return preds, probs


class TinyCNN(nn.Module):
    """
    Very small CNN for quick CPU training. Works with any input size.
    """
    def __init__(self, num_classes: int = 247, dropout: float = 0.3):
        super().__init__()
        self.num_classes = num_classes
        
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        # Adaptive pooling to fixed 4x4 — works for any input size
        self.adaptive_pool = nn.AdaptiveAvgPool2d(4)
        
        self.fc1 = nn.Linear(64 * 4 * 4, 256)
        self.fc2 = nn.Linear(256, num_classes)
        self.dropout = nn.Dropout(dropout)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.relu(self.conv3(x))
        x = self.adaptive_pool(x)           # -> (batch, 64, 4, 4)
        x = x.flatten(1)                    # -> (batch, 64*4*4)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        return x


class TamilCRNN(nn.Module):
    """
    CRNN (CNN + RNN + CTC) for sequence recognition of Tamil characters.
    
    Architecture:
    - CNN: Feature extractor (ResNet-like)
    - RNN: Sequence modeling (Bidirectional LSTM)
    - FC: Mapping to character classes
    
    Input: (batch, 1, height, width) - standard height is 32 or 64
    Output: (seq_len, batch, num_classes) - log probabilities for CTC loss
    """
    
    def __init__(self, num_classes: int = 248, dropout: float = 0.2):
        super().__init__()
        
        self.num_classes = num_classes
        
        # CNN Feature Extractor (Reduced ResNet)
        self.cnn = nn.Sequential(
            ConvBlock(1, 64, kernel_size=3, stride=1, padding=1),
            nn.MaxPool2d(2, 2),  # -> 32x32
            
            ConvBlock(64, 128, kernel_size=3, stride=1, padding=1),
            ResidualBlock(128),
            nn.MaxPool2d(2, 2),  # -> 16x16
            
            ConvBlock(128, 256, kernel_size=3, stride=1, padding=1),
            ResidualBlock(256),
            nn.MaxPool2d((2, 1), (2, 1)), # -> 8x16 (keep horizontal resolution)
            
            ConvBlock(256, 512, kernel_size=3, stride=1, padding=1),
            ResidualBlock(512),
            nn.MaxPool2d((2, 1), (2, 1)), # -> 4x16
            
            nn.Conv2d(512, 512, kernel_size=(4, 1), stride=1, padding=0), # -> 1x16
        )
        
        self.rnn = nn.LSTM(512, 256, bidirectional=True, num_layers=2, dropout=dropout)
        
        # num_classes + 1 for the CTC blank token
        self.fc = nn.Linear(512, num_classes + 1)
        
        self._init_weights()
    
    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)

    def forward(self, x):
        # x shape: (batch, 1, height, width)
        conv = self.cnn(x)
        
        # Reshape for RNN
        # conv shape: (batch, channels, h, w)
        # We want to treat the width as the sequence dimension
        b, c, h, w = conv.size()
        assert h == 1, f"Height after CNN must be 1, got {h}"
        
        conv = conv.squeeze(2) # (batch, channels, width)
        conv = conv.permute(2, 0, 1) # (width, batch, channels)
        
        # RNN
        output, _ = self.rnn(conv)
        
        # Classifier
        # output shape: (seq_len, batch, 512)
        logits = self.fc(output)
        
        return logits


def create_model(model_type: str = "cnn", num_classes: int = 247, pretrained_path: str = None) -> nn.Module:
    """
    Create a Vatteluttu model (CNN or CRNN).
    
    Args:
        model_type: "cnn" or "crnn"
        num_classes: Number of output classes
        pretrained_path: Path to pretrained weights (optional)
    
    Returns:
        Model instance
    """
    if model_type.lower() == "cnn":
        model = VatteluttuCNN(num_classes=num_classes)
    elif model_type.lower() == "tiny_cnn":
        model = TinyCNN(num_classes=num_classes)
    elif model_type.lower() == "crnn":
        model = TamilCRNN(num_classes=num_classes)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    if pretrained_path:
        try:
            state_dict = torch.load(pretrained_path, map_location='cpu')
            model.load_state_dict(state_dict)
            print(f"Loaded pretrained weights from {pretrained_path}")
        except Exception as e:
            print(f"Could not load pretrained weights: {e}")
    
    return model


if __name__ == "__main__":
    # Test CNN
    cnn = create_model("cnn", num_classes=247)
    print(f"CNN created with {sum(p.numel() for p in cnn.parameters()):,} parameters")
    x_cnn = torch.randn(4, 1, 64, 64)
    y_cnn = cnn(x_cnn)
    print(f"CNN Input shape: {x_cnn.shape} -> Output shape: {y_cnn.shape}")
    
    # Test CRNN
    crnn = create_model("crnn", num_classes=216)
    print(f"\nCRNN created with {sum(p.numel() for p in crnn.parameters()):,} parameters")
    # CRNN expects width > height usually for sequences
    x_crnn = torch.randn(4, 1, 32, 128)
    try:
        y_crnn = crnn(x_crnn)
        print(f"CRNN Input shape: {x_crnn.shape} -> Output shape: {y_crnn.shape}")
    except Exception as e:
        print(f"CRNN test failed: {e}")
