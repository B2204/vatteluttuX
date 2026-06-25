/**
 * VatteluttuX - Character Table Component
 * 
 * Display per-character predictions with hover effects.
 */
import { useState } from 'react';
import type { CharacterPrediction } from '../types';
import './CharacterTable.css';

interface CharacterTableProps {
    characters: CharacterPrediction[];
    onCharacterHover?: (index: number | null) => void;
}

export function CharacterTable({ characters, onCharacterHover }: CharacterTableProps) {
    const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

    const handleMouseEnter = (index: number) => {
        setHoveredIndex(index);
        onCharacterHover?.(index);
    };

    const handleMouseLeave = () => {
        setHoveredIndex(null);
        onCharacterHover?.(null);
    };

    const getConfidenceClass = (confidence: number): string => {
        if (confidence >= 0.9) return 'confidence-high';
        if (confidence >= 0.7) return 'confidence-medium';
        return 'confidence-low';
    };

    if (characters.length === 0) {
        return (
            <div className="character-table-empty">
                <p>No characters detected</p>
            </div>
        );
    }

    return (
        <div className="character-table-container">
            <h3>Character Predictions</h3>
            <div className="table-wrapper">
                <table className="character-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Tamil</th>
                            <th>Label</th>
                            <th>Confidence</th>
                            <th>Position</th>
                        </tr>
                    </thead>
                    <tbody>
                        {characters.map((char, index) => (
                            <tr
                                key={index}
                                className={hoveredIndex === index ? 'hovered' : ''}
                                onMouseEnter={() => handleMouseEnter(index)}
                                onMouseLeave={handleMouseLeave}
                            >
                                <td className="cell-index">{index + 1}</td>
                                <td className="cell-tamil">{char.modern_tamil}</td>
                                <td className="cell-label">{char.label}</td>
                                <td className="cell-confidence">
                                    <span className={`confidence-badge ${getConfidenceClass(char.confidence)}`}>
                                        {(char.confidence * 100).toFixed(1)}%
                                    </span>
                                </td>
                                <td className="cell-bbox">
                                    ({char.bbox[0]}, {char.bbox[1]})
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="table-footer">
                <span className="legend">
                    <span className="confidence-badge confidence-high">High ≥90%</span>
                    <span className="confidence-badge confidence-medium">Medium ≥70%</span>
                    <span className="confidence-badge confidence-low">Low &lt;70%</span>
                </span>
            </div>
        </div>
    );
}
