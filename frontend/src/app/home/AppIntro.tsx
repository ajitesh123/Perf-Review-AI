import { Switch } from '@components/ui/switch';
import React, { useState } from 'react';
import { isPerfReviewType, ReviewType } from '@constants/common';
import GradientBackground from '@components/GradientBackground';
import { TextButton } from '@components/ui/button';

const GradientColor = {
  perfReview: {
    fromColor: '#ff80b5',
    toColor: '#9089fc',
  },
  selfReview: {
    fromColor: '#bbf7d0',
    toColor: '#166534',
  },
};

const AppIntro = ({ reviewType, onReviewTypeChange }: any) => {
  const [isChecked, setIsChecked] = useState(!isPerfReviewType(reviewType));
  const [fromColor, setFromColor] = useState(
    isPerfReviewType(reviewType)
      ? GradientColor.perfReview.fromColor
      : GradientColor.selfReview.fromColor
  );
  const [toColor, setToColor] = useState(
    isPerfReviewType(reviewType)
      ? GradientColor.perfReview.toColor
      : GradientColor.selfReview.toColor
  );

  const handleReviewTypeChange = (checked: boolean) => {
    setIsChecked(checked);
    if (checked) {
      onReviewTypeChange(ReviewType.selfReview);
      setFromColor(GradientColor.selfReview.fromColor);
      setToColor(GradientColor.selfReview.toColor);
    } else {
      onReviewTypeChange(ReviewType.perfReview);
      setFromColor(GradientColor.perfReview.fromColor);
      setToColor(GradientColor.perfReview.toColor);
    }
  };

  return (
    <section className="relative isolate px-6 pt-2 lg:px-8 widget-animate animate in-view">
      <GradientBackground fromColor={fromColor} toColor={toColor} />
      <div className="mx-auto max-w-6xl pb-12 pt-36">
        <div className="flex flex-col items-center">
          {/* <div className="mt-10 flex items-center justify-center md:gap-x-16 gap-x-8">
            <TextButton
              variant={`primary-${
                isPerfReviewType(reviewType) ? 'perf' : 'self'
              }-review`}
              loading
            >
              Try Now
            </TextButton>
            <TextButton
              variant={`primary-${
                isPerfReviewType(reviewType) ? 'perf' : 'self'
              }-review`}
            >
              Try Now
            </TextButton>
            <TextButton
              variant={`primary-${
                isPerfReviewType(reviewType) ? 'perf' : 'self'
              }-review`}
              disabled
            >
              Try Now
            </TextButton>
            <TextButton variant="secondary">Try Now</TextButton>
            <TextButton variant="secondary" disabled>
              Try Now
            </TextButton>
          </div> */}
          <h1 className="text-4xl font-bold text-center text-gray-200 tracking-tight sm:text-5xl">
            Performance Review Assistant
          </h1>
          <p className="mt-6 font-bold leading-8 text-slate-300">
            Voice-First | AI-Powered | Incredibly Simple
          </p>

          <div
            className="mt-12 flex flex-1 items-center max-w-3xl p-0 align-middle gap-4"
            role="tablist"
            aria-orientation="horizontal"
          >
            <span
              className="
                text-sm
                font-semibold
                text-milk"
            >
              {ReviewType.perfReview}
            </span>
            <Switch
              size="xl"
              checked={isChecked}
              onChange={handleReviewTypeChange}
            />
            <span
              className="
                text-sm
                font-semibold
                text-milk"
            >
              {ReviewType.selfReview}
            </span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AppIntro;
