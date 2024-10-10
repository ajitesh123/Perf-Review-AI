export const isObject = (data: unknown): data is Record<string, unknown> =>
  typeof data === 'object' && data !== null && !Array.isArray(data);

export const isObjectAndNotBlank = (
  data: unknown
): data is Record<string, unknown> =>
  isObject(data) && Object.keys(data).length > 0;

export const isBlankObject = (data: unknown): data is Record<string, never> =>
  isObject(data) && Object.keys(data).length === 0;

export const hasOwnPropertySafe = (data: unknown, property: string): boolean =>
  isObject(data) && Object.prototype.hasOwnProperty.call(data, property);

export const isEmptyArray = (array: unknown): array is [] =>
  Array.isArray(array) && array.length === 0;
