import React, { useState, useRef } from "react";
import "./style.css"; // Assume you have some styles for basic setup

const App = () => {
  const [currentIndex, setCurrentIndex] = useState(1);
  const blocksRef = useRef([]);

  const blocks = [
    { id: 0, content: "Block 1" },
    { id: 1, content: "Block 2" },
    { id: 2, content: "Block 3" },
    { id: 3, content: "Block 4" },
    { id: 4, content: "Block 5" },
  ];

  const handleNext = () => {
    if (currentIndex < blocks.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  return (
    <div className="app-container">
      <div className="content-container">
        {blocks.map((block, index) => (
          <div
            key={block.id}
            className={`block ${currentIndex === index ? "highlighted" : ""}`}
            ref={(el) => (blocksRef.current[index] = el)}
          >
            {block.content}
          </div>
        ))}
      </div>

      {currentIndex >= 0 && (
        <div
          className="coachmark"
          style={{
            top: blocksRef.current[currentIndex]?.offsetTop + 10 || 0,
            left: blocksRef.current[currentIndex]?.offsetLeft || 0,
          }}
        >
          <div className="coachmark-content">
            <p>Currently highlighting: {blocks[currentIndex].content}</p>
            <div className="button-container">
              <button onClick={handlePrev} disabled={currentIndex === 0}>
                Back
              </button>
              <button
                onClick={handleNext}
                disabled={currentIndex === blocks.length - 1}
              >
                Next
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="overlay" />
    </div>
  );
};

export default App;
