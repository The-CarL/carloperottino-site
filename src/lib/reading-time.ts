/**
 * Estimate reading time in minutes for a given text.
 * Uses 238 wpm (average adult reading speed for technical content).
 */
export function getReadingTime(text: string): string {
  const words = text.trim().split(/\s+/).length;
  const minutes = Math.max(1, Math.round(words / 238));
  return `${minutes} min read`;
}
