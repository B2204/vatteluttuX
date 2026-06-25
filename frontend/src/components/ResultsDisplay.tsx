/**
 * VatteluttuX - Results Display Component
 * 
 * Show recognition results with traced image and export options.
 */
import { useState } from 'react';
import type { RecognitionResponse } from '../types';
import { CharacterTable } from './CharacterTable';
import { getTracedImageUrl } from '../utils/api';
import './ResultsDisplay.css';

interface ResultsDisplayProps {
    result: RecognitionResponse;
}

export function ResultsDisplay({ result }: ResultsDisplayProps) {
    const [copySuccess, setCopySuccess] = useState(false);
    const [highlightedChar, setHighlightedChar] = useState<number | null>(null);

    const copyToClipboard = async () => {
        try {
            await navigator.clipboard.writeText(result.modern_text);
            setCopySuccess(true);
            setTimeout(() => setCopySuccess(false), 2000);
        } catch (err) {
            console.error('Failed to copy:', err);
        }
    };

    const exportAsText = () => {
        const blob = new Blob([result.modern_text], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'vatteluttu_recognition.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    const exportAsJson = () => {
        const exportData = {
            recognized_text: result.recognized_text,
            modern_text: result.modern_text,
            words: result.words,
            characters: result.characters,
            timestamp: new Date().toISOString()
        };
        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'vatteluttu_recognition.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    return (
        <div className="results-display">
            {/* Warnings */}
            {result.warnings.length > 0 && (
                <div className="warnings-section">
                    {result.warnings.map((warning, idx) => (
                        <div key={idx} className="warning-item">
                            ⚠️ {warning}
                        </div>
                    ))}
                </div>
            )}

            {/* Main Result */}
            <div className="result-main">
                <h2>Recognized Tamil Text</h2>
                <div className="tamil-text-display">
                    <span className="tamil-text" style={{ whiteSpace: 'pre-wrap' }}>
                        {result.modern_text || '(No text recognized)'}
                    </span>
                </div>

                {/* Stats */}
                {(result.num_words > 0 || result.num_characters > 0) && (
                    <div className="recognition-stats" style={{
                        display: 'flex', gap: '1rem', marginTop: '0.5rem',
                        fontSize: '0.85rem', color: '#9ca3af'
                    }}>
                        {result.num_characters > 0 && (
                            <span>📝 {result.num_characters} character{result.num_characters !== 1 ? 's' : ''}</span>
                        )}
                        {result.num_words > 0 && (
                            <span>📖 {result.num_words} word{result.num_words !== 1 ? 's' : ''}</span>
                        )}
                    </div>
                )}

                <div className="action-buttons">
                    <button className="btn btn-primary" onClick={copyToClipboard}>
                        {copySuccess ? '✓ Copied!' : '📋 Copy Text'}
                    </button>
                    <button className="btn btn-secondary" onClick={exportAsText}>
                        📄 Export .txt
                    </button>
                    <button className="btn btn-secondary" onClick={exportAsJson}>
                        📦 Export .json
                    </button>
                </div>
            </div>

            {/* Word Results */}
            {result.words && result.words.length > 0 && (
                <div className="word-results-section" style={{ marginTop: '1.5rem' }}>
                    <h3>Word Detection</h3>
                    <div className="word-results-grid" style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
                        gap: '0.75rem',
                        marginTop: '0.75rem'
                    }}>
                        {result.words.map((word, idx) => (
                            <div key={idx} className="word-card" style={{
                                background: 'rgba(255,255,255,0.05)',
                                border: word.is_validated ? '1px solid rgba(34,197,94,0.3)' : '1px solid rgba(234,179,8,0.3)',
                                borderRadius: '8px',
                                padding: '0.75rem'
                            }}>
                                <div style={{ fontSize: '1.3rem', fontWeight: 600, marginBottom: '0.25rem' }}>
                                    {word.text}
                                </div>
                                <div style={{ fontSize: '0.8rem', color: '#9ca3af' }}>
                                    {word.num_characters} char{word.num_characters !== 1 ? 's' : ''} ·
                                    {' '}{(word.confidence * 100).toFixed(1)}% conf
                                </div>
                                <div style={{
                                    marginTop: '0.4rem',
                                    height: '3px',
                                    background: 'rgba(255,255,255,0.1)',
                                    borderRadius: '2px',
                                    overflow: 'hidden'
                                }}>
                                    <div style={{
                                        width: `${word.confidence * 100}%`,
                                        height: '100%',
                                        background: word.confidence > 0.7 ? '#22c55e' : word.confidence > 0.4 ? '#eab308' : '#ef4444',
                                        borderRadius: '2px'
                                    }} />
                                </div>
                                {word.validation_warnings.length > 0 && (
                                    <div style={{ fontSize: '0.7rem', color: '#eab308', marginTop: '0.3rem' }}>
                                        ⚠ {word.validation_warnings[0]}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Two Column Layout */}
            <div className="results-grid">
                {/* Traced Image */}
                <div className="traced-image-section">
                    <h3>Traced Image</h3>
                    {result.traced_image_path ? (
                        <div className="traced-image-container">
                            <img
                                src={getTracedImageUrl(result.traced_image_path)}
                                alt="Traced inscription with bounding boxes"
                                className="traced-image"
                                onError={(e) => {
                                    (e.target as HTMLImageElement).src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200"><rect fill="%231a1a2e" width="400" height="200"/><text x="200" y="100" fill="%236b7280" text-anchor="middle">Image not available</text></svg>';
                                }}
                            />
                            {highlightedChar !== null && result.characters[highlightedChar] && (
                                <div
                                    className="highlight-overlay"
                                    style={{
                                        left: `${(result.characters[highlightedChar].bbox[0] / result.image_width) * 100}%`,
                                        top: `${(result.characters[highlightedChar].bbox[1] / result.image_height) * 100}%`,
                                        width: `${(result.characters[highlightedChar].bbox[2] / result.image_width) * 100}%`,
                                        height: `${(result.characters[highlightedChar].bbox[3] / result.image_height) * 100}%`,
                                    }}
                                />
                            )}
                        </div>
                    ) : (
                        <div className="no-traced-image">
                            <p>Traced image not available</p>
                        </div>
                    )}
                    <p className="image-info">
                        Image size: {result.image_width} × {result.image_height}px
                    </p>
                </div>

                {/* Character Table */}
                <CharacterTable
                    characters={result.characters}
                    onCharacterHover={setHighlightedChar}
                />
            </div>

            {/* Label Sequence */}
            <div className="label-sequence-section">
                <h3>Label Sequence</h3>
                <code className="label-sequence">{result.recognized_text}</code>
            </div>
        </div>
    );
}
