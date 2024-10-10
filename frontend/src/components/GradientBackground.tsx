import React from 'react';

const GradientBackground = React.memo(
  ({ fromColor, toColor }: { fromColor: string; toColor: string }) => {
    const gradientStyle = React.useMemo(
      () => ({
        backgroundImage: `linear-gradient(to right, ${fromColor}, ${toColor})`,
        clipPath:
          'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
      }),
      [fromColor, toColor]
    );

    return (
      <div
        className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80"
        aria-hidden="true"
      >
        <div
          className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"
          style={gradientStyle}
        />
      </div>
    );
  }
);

GradientBackground.displayName = 'GradientBackground';

export default GradientBackground;
