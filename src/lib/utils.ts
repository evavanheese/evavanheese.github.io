import { profile } from '../settings'
import { template } from '../settings'

// Matches all reasonable variants of the author's name:
// Eva van Heese, Eva M. van Heese, E. van Heese, E.M. van Heese, E. M. van Heese
const AUTHOR_PATTERN = /\bE(?:va)?\.?\s*M?\.?\s*van\s+Heese\b/g;

export function highlightAuthor(authors: string): string {
  if (AUTHOR_PATTERN.test(authors)) {
    AUTHOR_PATTERN.lastIndex = 0;
    return authors.replace(
      AUTHOR_PATTERN,
      (match) => `<span class='font-bold text-primary'>${match}</span>`
    );
  }
  return authors;
}

export function trimExcerpt(excerpt: string): string {
  const excerptLength = template.excerptLength
  return excerpt.length > excerptLength ? `${excerpt.substring(0, excerptLength)}...` : excerpt
}
