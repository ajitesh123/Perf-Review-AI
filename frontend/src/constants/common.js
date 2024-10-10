const ReviewType = {
  perfReview: 'Performance Review',
  selfReview: 'Self Review',
};

const isPerfReviewType = (reviewType) => reviewType === ReviewType.perfReview;

export { ReviewType, isPerfReviewType };
