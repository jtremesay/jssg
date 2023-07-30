/**
 * @brief A linear interpolation
 * @param x The value to interpolate
 * @param x0 First reference
 * @param x1 Second reference
 * @param y0 Result of f(x0)
 * @param y1 Result of f(x1)
 * @returns the interpolated value
 */
export function lerp(x: number, x0: number, x1: number, y0: number, y1: number): number {
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0);
}