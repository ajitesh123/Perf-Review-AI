import { ButtonHTMLAttributes, forwardRef } from 'react';
import { Spinner } from '../spinner/spinner';
import { buildClassNames } from '@utils/classnames';

type Variant =
  | 'basic'
  | 'primary-perf-review'
  | 'primary-self-review'
  | 'secondary'
  | 'destructive'
  | 'custom';

interface ColorConfig {
  default: string;
  disabled?: string;
}

const colorConfigs: Record<Variant, ColorConfig> = {
  custom: {
    default: '',
  },
  basic: {
    default: '',
  },
  'primary-perf-review': {
    default: 'border bg-violet-500 hover:bg-violet-600 text-milk',
    disabled: 'bg-violet-600 opacity-70 text-gray-400',
  },
  'primary-self-review': {
    default: 'border bg-teal-500 hover:bg-teal-600 text-milk',
    disabled: 'bg-teal-600 opacity-70 text-gray-400',
  },
  secondary: {
    default: 'border border-gray-500 hover:bg-neutral-800 text-milk',
    disabled: 'opacity-70 border-gray-600 text-gray-600',
  },
  destructive: {
    default: '',
  },
};

const sizeConfigs = {
  xs: 'min-h-4 h-4',
  sm: 'min-h-6 h-6',
  md: 'min-h-8 h-8',
  lg: 'min-h-11 h-11',
};

export type ButtonSize = 'lg' | 'md' | 'sm' | 'xs';

export interface BaseBtnProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  loading?: boolean;
  size?: ButtonSize;
  variant?: Variant;
}

export const BaseButton = forwardRef<HTMLButtonElement, BaseBtnProps>(
  function Button(props, ref) {
    const {
      size = 'lg',
      loading,
      variant = 'basic',
      className,
      children,
      onClick,
      ...rest
    } = props;

    const buttonClasses = buildClassNames(
      'relative rounded-md font-medium',
      colorConfigs[variant].default,
      rest.disabled
        ? `${colorConfigs[variant].disabled || ''} cursor-not-allowed`
        : 'hover:bg-none',
      loading ? 'cursor-progress' : '',
      sizeConfigs[size],
      className
    );

    return (
      <button
        type="button"
        {...rest}
        className={buttonClasses}
        ref={ref}
        onClick={(event) => {
          if (!loading) {
            onClick?.(event);
          }
        }}
      >
        {/* {loading && (
          <span className="absolute-center">
            <Spinner size={size} data-testid="spinner-icon" />
          </span>
        )} */}
        <div
          data-testid="button-content"
          className={buildClassNames(
            'flex items-center',
            loading ? 'invisible' : 'visible'
          )}
        >
          {children}
        </div>
      </button>
    );
  }
);
