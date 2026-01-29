import React, { useState } from 'react';

export default function Root({ children }) {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const askAI = async () => {
    if (!input) return;
    setResponse("Wait, thinking...");
    try {
      // ✅ Yahan humne aapka Vercel domain daal diya hai
      const res = await fetch(`https://physical-ai-book-n7kz.vercel.app/chat?query=${encodeURIComponent(input)}`);
      const data = await res.json();
      setResponse(data.answer);
    } catch (err) {
      setResponse("Backend se rabta nahi ho pa raha! Shayad server so raha hai.");
    }
  };

  return (
    <>
      {children}
      {/* Floating Chat Button */}
      <div style={{ position: 'fixed', bottom: 30, right: 30, zIndex: 1000 }}>
        <button 
          onClick={() => setOpen(!open)}
          style={{ width: 60, height: 60, borderRadius: '50%', backgroundColor: '#25c2a0', color: 'white', border: 'none', cursor: 'pointer', fontSize: '30px', boxShadow: '0 4px 10px rgba(0,0,0,0.3)' }}
        >
          {open ? '×' : '💬'}
        </button>
        
        {/* Chat Window */}
        {open && (
          <div style={{ position: 'absolute', bottom: 80, right: 0, width: 320, background: 'white', border: '1px solid #ddd', borderRadius: 15, padding: 20, boxShadow: '0 10px 25px rgba(0,0,0,0.2)', color: '#333' }}>
            <h3 style={{ margin: '0 0 10px 0', color: '#25c2a0' }}>Physical AI Bot</h3>
            <p style={{ fontSize: '12px', color: '#666' }}>Panaversity Hackathon Edition</p>
            <hr />
            <input 
              value={input} 
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && askAI()}
              placeholder="Ask about ROS2 or Robots..." 
              style={{ width: '100%', marginBottom: 10, padding: 10, borderRadius: 5, border: '1px solid #ddd' }}
            />
            <button onClick={askAI} style={{ width: '100%', backgroundColor: '#25c2a0', color: 'white', border: 'none', padding: 10, borderRadius: 5, cursor: 'pointer', fontWeight: 'bold' }}>Ask AI</button>
            <div style={{ marginTop: 15, padding: 10, backgroundColor: '#f9f9f9', borderRadius: 5, fontSize: '14px', minHeight: '50px', maxHeight: '200px', overflowY: 'auto' }}>
              <strong>AI:</strong> {response}
            </div>
          </div>
        )}
      </div>
    </>
  );
}