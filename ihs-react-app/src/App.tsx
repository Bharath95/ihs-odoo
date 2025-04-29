// src/App.tsx
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import HomePage from '@/pages/HomePage';
import AboutPage from '@/pages/AboutPage';
import AdmissionRegistrationPage from '@/pages/AdmissionRegistrationPage';
import DarkModeToggle from '@/components/DarkModeToggle';
import { useTheme } from '@/hooks/useTheme'; // Import the hook

function App() {
  useTheme(); // Initialize theme listener and application

  return (
    <Router>
      {/* Rest of the App component remains the same... */}
      <div className="min-h-screen flex flex-col">
        <header className="container mx-auto py-4 px-6 flex justify-between items-center border-b">
          <nav className="flex gap-4">
            <Link to="/" className="text-lg font-semibold hover:text-primary">Home</Link>
            <Link to="/about" className="text-lg font-semibold hover:text-primary">About</Link>
            <Link to="/admission" className="text-lg font-semibold hover:text-primary">Admission</Link>
          </nav>
          <DarkModeToggle />
        </header>
        <main className="flex-grow container mx-auto py-8 px-6">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/admission" element={<AdmissionRegistrationPage />} /> 
          </Routes>
        </main>
        <footer className="container mx-auto py-4 px-6 text-center text-muted-foreground text-sm border-t">
          © {new Date().getFullYear()} My PWA Starter
        </footer>

      </div>
    </Router>
  );
}

export default App;