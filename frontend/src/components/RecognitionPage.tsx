/**
 * VatteluttuX - Recognition Page Component
 * 
 * Main page combining upload, recognition, and results.
 */
import { useState, useCallback, useRef, useEffect } from 'react';
import type { RecognitionState } from '../types';
import { UploadPanel } from './UploadPanel';
import { ResultsDisplay } from './ResultsDisplay';
import { recognizeImage } from '../utils/api';
import './RecognitionPage.css';

export function RecognitionPage() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [state, setState] = useState<RecognitionState>({ status: 'idle' });
    const resultsRef = useRef<HTMLDivElement>(null);

    const handleFileSelect = useCallback((file: File | null) => {
        setSelectedFile(file);
        setState({ status: 'idle' });
    }, []);

    const handleRecognize = async () => {
        if (!selectedFile) return;

        setState({ status: 'loading' });

        try {
            const result = await recognizeImage(selectedFile);
            setState({ status: 'success', data: result });
        } catch (error) {
            setState({
                status: 'error',
                message: error instanceof Error ? error.message : 'Recognition failed',
            });
        }
    };

    // Scroll to results when available
    useEffect(() => {
        if (state.status === 'success' && resultsRef.current) {
            setTimeout(() => {
                resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);
        }
    }, [state.status]);

    return (
        <div className="recognition-page">
            {/* Upload Section */}
            <section className="upload-section">
                <UploadPanel
                    onFileSelect={handleFileSelect}
                    selectedFile={selectedFile}
                    isLoading={state.status === 'loading'}
                />

                {/* Recognize Button */}
                <div className="recognize-section">
                    <button
                        className="recognize-btn"
                        onClick={handleRecognize}
                        disabled={!selectedFile || state.status === 'loading'}
                    >
                        {state.status === 'loading' ? (
                            <>
                                <span className="spinner"></span>
                                Recognizing...
                            </>
                        ) : (
                            <>
                                <span className="btn-icon">🔍</span>
                                Recognize Inscription
                            </>
                        )}
                    </button>

                    {selectedFile && state.status === 'idle' && (
                        <p className="helper-text">
                            Click the button above to start OCR recognition
                        </p>
                    )}
                </div>
            </section>

            {/* Error State */}
            {state.status === 'error' && (
                <section className="error-section">
                    <div className="error-message">
                        <span className="error-icon">❌</span>
                        <div>
                            <h3>Recognition Failed</h3>
                            <p>{state.message}</p>
                        </div>
                    </div>
                    <button className="retry-btn" onClick={handleRecognize}>
                        Try Again
                    </button>
                </section>
            )}

            {/* Results Section */}
            {state.status === 'success' && (
                <section className="results-section" ref={resultsRef}>
                    <ResultsDisplay result={state.data} />
                </section>
            )}
        </div>
    );
}
