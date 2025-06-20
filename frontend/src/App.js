import React, { useEffect } from "react";
import reportWebVitals from './reportWebVitals';
import GenUIRenderer from "./components/GenUI/GenUIRenderer";
import { logUserEvent } from './data/eventLogger';

function App() {
  useEffect(() => {
    const handleClick = (e) => {
      logUserEvent('click', { x: e.clientX, y: e.clientY, target: e.target.tagName });
    };
    const handleScroll = () => {
      logUserEvent('scroll', { scrollY: window.scrollY });
    };
    window.addEventListener('click', handleClick);
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('click', handleClick);
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <div>
      <h2>Real-Time Generative UI Demo</h2>
      <GenUIRenderer/>
    </div>
  );
}

export default App;
