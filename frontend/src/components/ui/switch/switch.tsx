// import CheckIcon from '@assets/icons/spinner.svg';
// import CloseIcon from '@assets/icons/close.svg';
import { buildClassNames } from 'src/utils/classnames';
import { SvgIcon } from '../svg-icon';
import { ButtonHTMLAttributes } from 'react';

const SIZE_CLASSES: Record<string, string> = {
  sm: 'w-8 min-w-[2rem] h-4 min-h-[1rem]',
  md: 'w-10 min-w-[2.5rem] h-5 min-h-[1.25rem]',
  lg: 'w-12 min-w-[3rem] h-6 min-h-[1.5rem]',
  xl: 'w-16 min-w-[4rem] h-8 min-h-[2.0rem]',
};

const CLOSE_ICON_PROPS: Record<string, { width: number; height: number }> = {
  sm: { width: 6, height: 6 },
  md: { width: 8, height: 8 },
  lg: { width: 10, height: 10 },
  xl: { width: 16, height: 16 },
};

const CHECK_ICON_PROPS: Record<string, { width: number; height: number }> = {
  sm: { width: 8, height: 8 },
  md: { width: 10, height: 10 },
  lg: { width: 14, height: 14 },
};

export interface SwitchProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'onChange'> {
  checked: boolean;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  onChange?: (checked: boolean) => void;
}
export const Switch = ({
  checked,
  size = 'md',
  className,
  disabled,
  onChange,
  ...rest
}: SwitchProps) => {
  const buttonClasses = buildClassNames(
    'flex rounded-full relative overflow-visible z-0',
    SIZE_CLASSES[size],
    disabled ? 'cursor-not-allowed' : '',
    className
  );

  const backgroundClassNames = buildClassNames(
    'rounded-full absolute left-[5%] top-[10%] w-[90%] h-4/5 z-[-1]',
    checked
      ? 'bg-teal-500' // for self review theme
      : 'bg-violet-600' // for perf review theme
  );

  const pointerClassNames = buildClassNames(
    'w-1/2 h-full bg-milk flex items-center justify-center',
    'border rounded-full transition duration-200 ease-in-out hover:shadow-[0_0_0_2px]',
    checked
      ? 'rtl:-translate-x-full translate-x-full border-azure hover:shadow-azure/50'
      : 'border-elephant-400 hover:shadow-elephant-400/50',
    disabled ? 'hover:shadow-none' : ''
  );

  return (
    <button
      {...rest}
      type="button"
      className={buttonClasses}
      aria-checked={checked}
      role="switch"
      disabled={disabled}
      onClick={() => onChange?.(!checked)}
    >
      <span className={backgroundClassNames}></span>
      <span className={pointerClassNames}>
        {/* {checked ? (
          <SvgIcon
            svg={CheckIcon}
            size="custom"
            width={CHECK_ICON_PROPS[size].width}
            height={CHECK_ICON_PROPS[size].height}
          />
        ) : (
          <SvgIcon
            svg={CheckIcon}
            size="custom"
            width={CLOSE_ICON_PROPS[size].width}
            height={CLOSE_ICON_PROPS[size].height}
          />
        )} */}
      </span>
    </button>
  );
};
