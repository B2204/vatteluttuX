/**
 * VatteluttuX - Upload Panel Component
 * 
 * Drag-and-drop file upload with preview.
 */
import { useCallback, useState, useRef } from 'react';
import './UploadPanel.css';

interface UploadPanelProps {
    onFileSelect: (file: File) => void;
    selectedFile: File | null;
    isLoading: boolean;
}

export function UploadPanel({ onFileSelect, selectedFile, isLoading }: UploadPanelProps) {
    const [isDragging, setIsDragging] = useState(false);
    const [preview, setPreview] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFile = useCallback((file: File) => {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file (PNG, JPG, etc.)');
            return;
        }

        // Create preview
        const reader = new FileReader();
        reader.onload = (e) => {
            setPreview(e.target?.result as string);
        };
        reader.readAsDataURL(file);

        onFileSelect(file);
    }, [onFileSelect]);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    }, [handleFile]);

    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const handleClick = () => {
        fileInputRef.current?.click();
    };

    const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    };

    const clearSelection = () => {
        setPreview(null);
        onFileSelect(null as unknown as File);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    return (
        <div className="upload-panel">
            <h2>Upload Inscription Image</h2>

            <div
                className={`drop-zone ${isDragging ? 'dragging' : ''} ${preview ? 'has-preview' : ''}`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onClick={handleClick}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleFileInput}
                    style={{ display: 'none' }}
                    disabled={isLoading}
                />

                {preview ? (
                    <div className="preview-container">
                        <img src={preview} alt="Preview" className="preview-image" />
                        <div className="preview-overlay">
                            <span className="file-name">{selectedFile?.name}</span>
                            <button
                                className="clear-btn"
                                onClick={(e) => { e.stopPropagation(); clearSelection(); }}
                                disabled={isLoading}
                            >
                                ✕ Clear
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="drop-content">
                        <div className="drop-icon">📜</div>
                        <p className="drop-text">
                            <strong>Drop your inscription image here</strong>
                            <br />
                            or click to browse
                        </p>
                        <p className="drop-hint">Supports PNG, JPG, JPEG, BMP</p>
                    </div>
                )}
            </div>
        </div>
    );
}
