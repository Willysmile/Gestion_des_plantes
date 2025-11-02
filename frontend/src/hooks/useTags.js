import { useState, useEffect } from 'react';
import { tagsAPI } from '../lib/api';

export default function useTags() {
  const [categories, setCategories] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all categories with tags
  const fetchCategories = async () => {
    try {
      setLoading(true);
      const response = await tagsAPI.getCategories();
      setCategories(response.data);
      
      // Flatten all tags
      const allTags = response.data.flatMap(cat => cat.tags);
      setTags(allTags);
      setError(null);
    } catch (err) {
      console.error('Erreur chargement tags:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Fetch all tags
  const fetchTags = async () => {
    try {
      setLoading(true);
      const response = await tagsAPI.getTags();
      setTags(response.data);
      setError(null);
    } catch (err) {
      console.error('Erreur chargement tags:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Get tags by category
  const getTagsByCategory = (categoryName) => {
    const category = categories.find(cat => cat.name === categoryName);
    return category ? category.tags : [];
  };

  // Get auto tags (location, health_status, light)
  const getAutoTagCategories = () => {
    const autoNames = ['Emplacement', 'État de la plante', 'Luminosité'];
    return categories.filter(cat => autoNames.includes(cat.name));
  };

  // Get manual tag categories
  const getManualTagCategories = () => {
    const manualNames = ['Type de plante', 'Besoins en eau', 'Difficulté', 'Taille', 'Toxicité', 'Particularités'];
    return categories.filter(cat => manualNames.includes(cat.name));
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  return {
    categories,
    tags,
    loading,
    error,
    fetchCategories,
    fetchTags,
    getTagsByCategory,
    getAutoTagCategories,
    getManualTagCategories,
  };
}
