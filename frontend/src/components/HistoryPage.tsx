/**
 * VatteluttuX - History Page Component
 * 
 * Displays recognition history from the MySQL database.
 */
import { useState, useEffect, useCallback } from 'react';
import type { HistoryItem } from '../types';
import { fetchHistory, deleteHistory, getTracedImageUrl } from '../utils/api';
import './HistoryPage.css';

export function HistoryPage() {
    const [history, setHistory] = useState<HistoryItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedItem, setSelectedItem] = useState<HistoryItem | null>(null);

    const loadHistory = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await fetchHistory();
            setHistory(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load history');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadHistory();
    }, [loadHistory]);

    const handleDelete = async (id: number, e: React.MouseEvent) => {
        e.stopPropagation();
        if (!confirm('Delete this recognition record?')) return;

        try {
            await deleteHistory(id);
            setHistory(prev => prev.filter(item => item.id !== id));
            if (selectedItem?.id === id) setSelectedItem(null);
        } catch (err) {
            alert(err instanceof Error ? err.message : 'Failed to delete');
        }
    };

    const formatDate = (dateStr: string) => {
        try {
            const date = new Date(dateStr);
            return date.toLocaleString('en-IN', {
                day: '2-digit',
                month: 'short',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
            });
        } catch {
            return dateStr;
        }
    };

    const getConfidenceClass = (conf: number) => {
        if (conf >= 0.8) return 'confidence-high';
        if (conf >= 0.5) return 'confidence-medium';
        return 'confidence-low';
    };

    if (loading) {
        return (
            <div className="history-page">
                <div className="history-loading">
                    <div className="loading-spinner"></div>
                    <p>Loading recognition history...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="history-page">
                <div className="history-error">
                    <span className="error-icon">⚠️</span>
                    <h3>Could not load history</h3>
                    <p>{error}</p>
                    <p className="error-hint">Make sure MySQL is running (XAMPP → Start MySQL)</p>
                    <button className="retry-btn" onClick={loadHistory}>Retry</button>
                </div>
            </div>
        );
    }

    return (
        <div className="history-page">
            <div className="history-header">
                <h2>📜 Recognition History</h2>
                <p className="history-subtitle">
                    {history.length} recognition{history.length !== 1 ? 's' : ''} saved in MySQL database
                </p>
                <button className="refresh-btn" onClick={loadHistory}>🔄 Refresh</button>
            </div>

            {history.length === 0 ? (
                <div className="history-empty">
                    <span className="empty-icon">📭</span>
                    <h3>No recognition history yet</h3>
                    <p>Go to OCR Recognition, upload an image, and your results will appear here.</p>
                </div>
            ) : (
                <div className="history-layout">
                    <div className="history-list">
                        {history.map(item => (
                            <div
                                key={item.id}
                                className={`history-card ${selectedItem?.id === item.id ? 'selected' : ''}`}
                                onClick={() => setSelectedItem(item)}
                            >
                                <div className="card-header">
                                    <span className="card-filename" title={item.original_filename}>
                                        📄 {item.original_filename}
                                    </span>
                                    <button
                                        className="delete-btn"
                                        onClick={(e) => handleDelete(item.id, e)}
                                        title="Delete record"
                                    >
                                        🗑️
                                    </button>
                                </div>
                                <div className="card-tamil-text">{item.modern_text || '—'}</div>
                                <div className="card-meta">
                                    <span className={`card-confidence ${getConfidenceClass(item.avg_confidence)}`}>
                                        {(item.avg_confidence * 100).toFixed(1)}% conf
                                    </span>
                                    <span className="card-chars">{item.num_characters} chars</span>
                                    <span className="card-words">{item.num_words} words</span>
                                </div>
                                <div className="card-date">{formatDate(item.created_at)}</div>
                            </div>
                        ))}
                    </div>

                    {selectedItem && (
                        <div className="history-detail">
                            <h3>Recognition Details</h3>
                            <div className="detail-grid">
                                <div className="detail-row">
                                    <span className="detail-label">File</span>
                                    <span className="detail-value">{selectedItem.original_filename}</span>
                                </div>
                                <div className="detail-row">
                                    <span className="detail-label">Modern Tamil</span>
                                    <span className="detail-value tamil-text">{selectedItem.modern_text}</span>
                                </div>
                                <div className="detail-row">
                                    <span className="detail-label">Labels</span>
                                    <span className="detail-value mono-text">{selectedItem.recognized_text}</span>
                                </div>
                                <div className="detail-row">
                                    <span className="detail-label">Characters</span>
                                    <span className="detail-value">{selectedItem.num_characters}</span>
                                </div>
                                <div className="detail-row">
                                    <span className="detail-label">Words</span>
                                    <span className="detail-value">{selectedItem.num_words}</span>
                                </div>
                                <div className="detail-row">
                                    <span className="detail-label">Avg Confidence</span>
                                    <span className={`detail-value ${getConfidenceClass(selectedItem.avg_confidence)}`}>
                                        {(selectedItem.avg_confidence * 100).toFixed(2)}%
                                    </span>
                                </div>
                                <div className="detail-row">
                                    <span className="detail-label">Date</span>
                                    <span className="detail-value">{formatDate(selectedItem.created_at)}</span>
                                </div>
                            </div>
                            {selectedItem.traced_image_path && (
                                <div className="detail-traced-image">
                                    <h4>Traced Image</h4>
                                    <img
                                        src={getTracedImageUrl(selectedItem.traced_image_path)}
                                        alt="Traced recognition"
                                        className="traced-img"
                                    />
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
