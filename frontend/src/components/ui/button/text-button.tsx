import { buildClassNames } from '@utils/classnames';
import { BaseButton, BaseBtnProps } from './base-button';
import { forwardRef } from 'react';

const sizeConfigs = {
  xs: 'text-xs px-0.5',
  sm: 'text-sm px-1',
  md: 'px-2',
  lg: 'text-sm px-4',
};

export interface TxtBtnProps extends BaseBtnProps {
  startIcon?: JSX.Element;
  endIcon?: JSX.Element;
}

export const TextButton = forwardRef<HTMLButtonElement, TxtBtnProps>(
  function TextButton(props: TxtBtnProps, ref) {
    const {
      className,
      children,
      startIcon,
      endIcon,
      size = 'lg',
      ...rest
    } = props;
    return (
      <BaseButton
        {...rest}
        ref={ref}
        size={size}
        className={buildClassNames(sizeConfigs[size], className)}
      >
        {startIcon && (
          <span className="pe-0.5" data-testid="start-icon">
            {startIcon}
          </span>
        )}
        <span className="flex-1 truncate px-1">{children}</span>
        {endIcon && (
          <span className="ps-0.5" data-testid="end-icon">
            {endIcon}
          </span>
        )}
      </BaseButton>
    );
  }
);
