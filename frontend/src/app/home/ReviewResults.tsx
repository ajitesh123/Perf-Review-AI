import { Key, useCallback, useState } from 'react';

interface ReviewItem {
  question: string;
  answer: string;
}

const ReviewResults = ({ reviews }: any) => {
  const [copyBtnText, setCopyBtnText] = useState('Copy');

  const handleCopyClick = useCallback(() => {
    setCopyBtnText('Copied!')

    // Get the parent div
    const parentDiv = document.getElementById("reviews");

    // Copy the content (HTML) of the parent div and its children
    const copiedContent = parentDiv?.innerText as string;

    // copy to clipboard
    navigator.clipboard.writeText(copiedContent);

    setTimeout(() => {
      setCopyBtnText('Copy')
    }, 1500);
  }, [setCopyBtnText]);

  return (
    <section className="relative isolate px-6 py-4 lg:py-8 lg:px-8 widget-animate animate in-view">
      <div className="flex flex-col mx-auto max-w-5xl justify-between gap-10">
        <div className="h-full w-full">
          <div className="border-secondary grid max-w-full gap-8 rounded-xl border bg-zinc-800 p-6 sm:p-12 sm:px-12 sm:text-base dark:bg-zinc-900">
            {reviews.length > 0 && (
              <div>
                <div className="flex flex-row justify-between mb-12">
                  <h2 className="font-semibold text-milk tracking-tight text-4xl">
                    Generated Review
                  </h2>
                  <div className="flex justify-end">
                    <span className="inline-flex items-center text-sm">
                      <button
                        type="button"
                        onClick={handleCopyClick}
                        className="inline-flex space-x-2 text-slate-500 hover:text-slate-300"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" aria-hidden="true" className="h-5 w-5">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path>
                        </svg>
                        <span className="font-medium">
                          {copyBtnText}
                        </span>
                      </button>
                    </span>
                  </div>
                </div>

                <div id='reviews'>
                  {reviews.map((item: ReviewItem, index: Key) => (
                    <div
                      key={index}
                      className="mb-12  border-b pb-8 border-gray-600"
                    >
                      <h3 className="text-milk text-lg font-medium mb-2">
                        {item.question}
                      </h3>
                      <p className="text-gray-300 leading-6 text-sm font-medium">
                        {item.answer}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};

export default ReviewResults;
