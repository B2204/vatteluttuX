/**
 * VatteluttuX - API Client
 * 
 * Functions for communicating with the FastAPI backend.
 */

import type { RecognitionResponse, HealthResponse, HistoryItem } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Check API health status.
 */
export async function checkHealth(): Promise<HealthResponse> {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
        throw new Error(`Health check failed: ${response.statusText}`);
    }
    return response.json();
}

/**
 * Send an image for OCR recognition.
 */
export async function recognizeImage(file: File): Promise<RecognitionResponse> {
    const formData = new FormData();
    formData.append('image', file);

    const response = await fetch(`${API_BASE_URL}/recognize`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Recognition failed: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Get full URL for a traced image path.
 */
export function getTracedImageUrl(path: string): string {
    if (path.startsWith('http')) {
        return path;
    }
    return `${API_BASE_URL}${path}`;
}

/**
 * Fetch all available labels from the backend.
 */
export async function fetchLabels(): Promise<Record<string, string>> {
    const response = await fetch(`${API_BASE_URL}/labels`);
    if (!response.ok) {
        throw new Error(`Failed to fetch labels: ${response.statusText}`);
    }
    const data = await response.json();
    return data.labels;
}

/**
 * Fetch recognition history from the database.
 */
export async function fetchHistory(skip = 0, limit = 50): Promise<HistoryItem[]> {
    const response = await fetch(`${API_BASE_URL}/history?skip=${skip}&limit=${limit}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch history: ${response.statusText}`);
    }
    return response.json();
}

/**
 * Delete a recognition history record.
 */
export async function deleteHistory(id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/history/${id}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error(`Failed to delete record: ${response.statusText}`);
    }
}

