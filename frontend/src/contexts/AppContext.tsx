'use client';

import React from 'react';
import { ReviewType } from '@constants/common';
import { createContext, useContext, useState, ReactNode } from 'react';

// Define the context shape
interface AppContextType {
  reviewType: string;
  updateReviewType: (newKeyValue: string) => void;
}

// Create the context
const AppContext = createContext<AppContextType | undefined>(undefined);

// Create the provider component
export function AppProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState({ reviewType: ReviewType.perfReview });

  // Function to update the reviewType
  const updateReviewType = (reviewType: string) => {
    setState((prevState) => ({
      ...prevState,
      reviewType,
    }));
  };

  return (
    <AppContext.Provider
      value={{ reviewType: state.reviewType, updateReviewType }}
    >
      {children}
    </AppContext.Provider>
  );
}

// Custom hook to use the AppContext
export function useAppContext() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
}
