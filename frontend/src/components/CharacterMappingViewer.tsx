/**
 * VatteluttuX - Character Mapping Viewer Component
 * 
 * Displays all 247 Tamil character mappings with filtering by category.
 */
import { useState, useEffect } from 'react';
import './CharacterMappingViewer.css';

interface CharacterInfo {
    label: string;
    modern_tamil: string;
    category: string;
    transliteration: string;
    description: string;
    base_consonant?: string;
    vowel_mark?: string;
}

interface CharacterMapData {
    total_characters: number;
    categories: {
        vowel: CharacterInfo[];
        aytham: CharacterInfo[];
        pure_consonant: CharacterInfo[];
        consonant: CharacterInfo[];
        uyirmei: CharacterInfo[];
    };
    statistics: {
        vowels: number;
        aytham: number;
        pure_consonants: number;
        consonants: number;
        uyirmei: number;
    };
}

export function CharacterMappingViewer() {
    const [characterMap, setCharacterMap] = useState<CharacterMapData | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedCategory, setSelectedCategory] = useState<string>('all');
    const [searchTerm, setSearchTerm] = useState<string>('');

    useEffect(() => {
        fetchCharacterMap();
    }, []);

    const fetchCharacterMap = async () => {
        try {
            setLoading(true);
            const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const response = await fetch(`${apiUrl}/character-map`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setCharacterMap(data);
            setError(null);
        } catch (err) {
            setError(`Failed to load character mappings: ${err instanceof Error ? err.message : 'Unknown error'}`);
        } finally {
            setLoading(false);
        }
    };

    const getFilteredCharacters = (): CharacterInfo[] => {
        if (!characterMap) return [];

        let characters: CharacterInfo[] = [];

        if (selectedCategory === 'all') {
            // Combine all categories
            characters = [
                ...characterMap.categories.vowel,
                ...characterMap.categories.aytham,
                ...characterMap.categories.pure_consonant,
                ...characterMap.categories.consonant,
                ...characterMap.categories.uyirmei
            ];
        } else {
            // Get specific category
            const category = selectedCategory as keyof typeof characterMap.categories;
            characters = characterMap.categories[category] || [];
        }

        // Apply search filter
        if (searchTerm) {
            const term = searchTerm.toLowerCase();
            characters = characters.filter(char =>
                char.label.toLowerCase().includes(term) ||
                char.modern_tamil.includes(searchTerm) ||
                char.transliteration.toLowerCase().includes(term) ||
                char.description.toLowerCase().includes(term)
            );
        }

        return characters;
    };

    if (loading) {
        return (
            <div className="character-mapping-viewer loading">
                <div className="spinner"></div>
                <p>Loading character mappings...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="character-mapping-viewer error">
                <div className="error-icon">⚠️</div>
                <p>{error}</p>
                <button onClick={fetchCharacterMap} className="retry-button">
                    Retry
                </button>
            </div>
        );
    }

    const filteredCharacters = getFilteredCharacters();

    return (
        <div className="character-mapping-viewer">
            <div className="viewer-header">
                <h2>Tamil Character Mappings</h2>
                <p className="subtitle">
                    Complete dataset of {characterMap?.total_characters} Vatteluttu to Modern Tamil character mappings
                </p>
            </div>

            {/* Statistics Cards */}
            {characterMap && (
                <div className="statistics-cards">
                    <div className="stat-card">
                        <div className="stat-number">{characterMap.statistics.vowels}</div>
                        <div className="stat-label">Vowels</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-number">{characterMap.statistics.pure_consonants}</div>
                        <div className="stat-label">Pure Consonants</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-number">{characterMap.statistics.consonants}</div>
                        <div className="stat-label">Consonants</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-number">{characterMap.statistics.uyirmei}</div>
                        <div className="stat-label">Uyirmei</div>
                    </div>
                </div>
            )}

            {/* Filters */}
            <div className="filters-section">
                <div className="filter-group">
                    <label htmlFor="category-filter">Category:</label>
                    <select
                        id="category-filter"
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        className="category-select"
                    >
                        <option value="all">All Categories ({characterMap?.total_characters})</option>
                        <option value="vowel">Vowels ({characterMap?.statistics.vowels})</option>
                        <option value="aytham">Aytham ({characterMap?.statistics.aytham})</option>
                        <option value="pure_consonant">Pure Consonants ({characterMap?.statistics.pure_consonants})</option>
                        <option value="consonant">Consonants ({characterMap?.statistics.consonants})</option>
                        <option value="uyirmei">Uyirmei ({characterMap?.statistics.uyirmei})</option>
                    </select>
                </div>

                <div className="filter-group">
                    <label htmlFor="search-filter">Search:</label>
                    <input
                        id="search-filter"
                        type="text"
                        placeholder="Search by label, Tamil, or transliteration..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="search-input"
                    />
                </div>
            </div>

            {/* Results Count */}
            <div className="results-info">
                Showing {filteredCharacters.length} character{filteredCharacters.length !== 1 ? 's' : ''}
            </div>

            {/* Character Grid */}
            <div className="character-grid">
                {filteredCharacters.map((char) => (
                    <div key={char.label} className={`character-card category-${char.category}`}>
                        <div className="char-tamil">{char.modern_tamil}</div>
                        <div className="char-label">{char.label}</div>
                        <div className="char-translit">{char.transliteration}</div>
                        <div className="char-description">{char.description}</div>
                        {char.base_consonant && (
                            <div className="char-composition">
                                {char.base_consonant} + {char.vowel_mark}
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {filteredCharacters.length === 0 && (
                <div className="no-results">
                    <p>No characters found matching your search.</p>
                </div>
            )}
        </div>
    );
}
