import { twMerge } from 'tailwind-merge';

export type ClassNamesCondition = Array<{
  condition: boolean;
  valid?: string;
  invalid?: string;
}>;

export type Classnames = Array<string | ClassNamesCondition | undefined>;

export const buildClassNames = (...args: Classnames): string => {
  const classList: string[] = [];
  args.forEach((arg) => {
    if (arg) {
      const argType = typeof arg;

      if (argType === 'string') {
        classList.push(arg as string);
      } else if (argType === 'object') {
        (arg as ClassNamesCondition).forEach(
          ({ condition, valid, invalid }) => {
            if (condition) {
              valid && classList.push(valid);
            } else {
              invalid && classList.push(invalid);
            }
          }
        );
      }
    }
  });
  return twMerge(classList.join(' '));
};
