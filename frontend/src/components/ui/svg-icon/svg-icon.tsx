import { FunctionComponent, SVGProps } from 'react';

export type Size = 'custom' | 'xs' | 'sm' | 'md' | 'lg' | 'xl';

export type SvgIconType = FunctionComponent<
  SVGProps<SVGSVGElement> & { title?: string }
>;

const SIZE_CLASSES: Record<Size, string> = {
  custom: '',
  xs: '8px',
  sm: '12px',
  md: '16px',
  lg: '20px',
  xl: '24px',
};

export interface SvgIconProps extends SVGProps<SVGSVGElement> {
  svg: SvgIconType;
  size?: Size;
}

export const SvgIcon = (props: SvgIconProps) => {
  const { svg: SvgElement, size, ...rest } = props;
  const sizeClasses = size ? SIZE_CLASSES[size] : SIZE_CLASSES.md;
  return (
    <SvgElement
      {...rest}
      className={props.className}
      height={sizeClasses || props.height}
      width={sizeClasses || props.width}
      style={{
        minHeight: sizeClasses || props.height,
        minWidth: sizeClasses || props.width,
      }}
    />
  );
};
