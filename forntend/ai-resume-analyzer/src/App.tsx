import { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { MainLayout } from '@/layouts/MainLayout';
import { ErrorBoundary } from '@/components/common/ErrorBoundary';
import { Skeleton } from '@/components/ui/Skeleton';

// Code Splitting: Lazy load major page components
const LandingPage = lazy(() => import('@/pages/LandingPage').then(module => ({ default: module.LandingPage })));
const AnalyzerPage = lazy(() => import('@/pages/AnalyzerPage').then(module => ({ default: module.AnalyzerPage })));

// Global Query Client Configuration for Production
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 10 * 60 * 1000, // Cache results for 10 minutes to save API calls
    },
  },
});

// Page Loader Fallback
const PageFallback = () => (
  <div className="container mx-auto p-8 space-y-6">
    <Skeleton className="h-12 w-3/4 max-w-md" />
    <Skeleton className="h-[400px] w-full" />
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <Skeleton className="h-48 w-full" />
      <Skeleton className="h-48 w-full col-span-2" />
    </div>
  </div>
);

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            <Route element={<MainLayout />}>
              <Route 
                path="/" 
                element={
                  <Suspense fallback={<PageFallback />}>
                    <LandingPage />
                  </Suspense>
                } 
              />
              <Route 
                path="/upload" 
                element={
                  <Suspense fallback={<PageFallback />}>
                    <AnalyzerPage />
                  </Suspense>
                } 
              />
            </Route>
          </Routes>
        </BrowserRouter>
        
        {/* Production Optimized Toaster */}
        <Toaster 
          position="bottom-right"
          toastOptions={{
            duration: 4000,
            className: '!bg-slate-900 !text-slate-100 !border !border-slate-800 shadow-xl',
          }} 
        />
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;