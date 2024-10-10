import SpinnerIcon from '@assets/icons/spinner.svg';
import { buildClassNames } from '@utils/classnames';
import { SvgIcon, SvgIconProps } from '../svg-icon/svg-icon';

export const Spinner = ({ className, ...rest }: Omit<SvgIconProps, 'svg'>) => {
  const defaultClasses = 'animate-spin';

  const classNames = buildClassNames(defaultClasses, className);
  return <SvgIcon {...rest} svg={SpinnerIcon} className={classNames} />;
};
