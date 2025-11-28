'use client';

import { useState, useEffect } from 'react';

interface LikeButtonProps {
  slug: string;
}

export function LikeButton({ slug }: LikeButtonProps) {
  const [likes, setLikes] = useState<number>(0);
  const [isLiked, setIsLiked] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Load initial like count and user's like status
  useEffect(() => {
    const loadLikes = async () => {
      try {
        const response = await fetch(`/api/likes/${slug}`);
        if (response.ok) {
          const data = await response.json();
          setLikes(data.likes || 0);

          // Check if user has already liked this post
          const hasLiked = localStorage.getItem(`liked-${slug}`) === 'true';
          setIsLiked(hasLiked);
        }
      } catch (error) {
        console.error('Failed to load likes:', error);
      }
    };

    loadLikes();
  }, [slug]);

  const handleLike = async () => {
    if (isLoading) return;

    setIsLoading(true);
    const newIsLiked = !isLiked;

    try {
      const response = await fetch(`/api/likes/${slug}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: newIsLiked ? 'like' : 'unlike'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setLikes(data.likes);
        setIsLiked(newIsLiked);

        // Save user's like status to localStorage
        localStorage.setItem(`liked-${slug}`, String(newIsLiked));
      }
    } catch (error) {
      console.error('Failed to update like:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center gap-2 my-8">
      <button
        onClick={handleLike}
        disabled={isLoading}
        className={`
          flex items-center gap-2 px-4 py-2 rounded-lg font-semibold
          transition-all duration-200
          ${isLiked
            ? 'bg-red-500 text-white hover:bg-red-600 dark:bg-red-600 dark:hover:bg-red-700'
            : 'bg-neutral-100 text-neutral-900 hover:bg-neutral-200 dark:bg-neutral-800 dark:text-neutral-100 dark:hover:bg-neutral-700'
          }
          ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        `}
        aria-label={isLiked ? 'Unlike this post' : 'Like this post'}
      >
        <svg
          className={`w-5 h-5 transition-transform ${isLiked ? 'scale-110' : ''}`}
          fill={isLiked ? 'currentColor' : 'none'}
          stroke="currentColor"
          strokeWidth={isLiked ? 0 : 2}
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
          />
        </svg>
        <span>{likes}</span>
      </button>
    </div>
  );
}
