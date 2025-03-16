import React, { useState } from "react";
import { Input } from "./components/Input";
import { Button } from "./components/Button";
import { Card, CardContent } from "./components/Card";
import { Send } from 'lucide-react';
import { AnimatedBackground } from 'animated-backgrounds';

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    try {
      if (input === "hi" || input === "Hi" || input === "hii" || input === "Hii") {
        const data = "Welcome to TourLanka. A chatbot providing scholarly information about the importance and history of Sri Lanka tourist destinations.!";
        const botMessage = { text: data, sender: "bot" };
        setMessages((prev) => [...prev, botMessage]);
      }else{
        const response = await fetch(`http://127.0.0.1:8000/?query=${encodeURIComponent(input)}`);
        const data = await response.json();
        const botMessage = { text: data.response, sender: "bot" };
        setMessages((prev) => [...prev, botMessage]);
      }
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <AnimatedBackground animationName="rainbowWaves" 
       blendMode="multiply " />
      <Card className="w-full max-w-2xl shadow-lg font-sans">
        <CardContent className="p-4 space-y-4 h-96 overflow-y-auto border-b">
          {messages.map((msg, index) => (
            <div key={index} className={`p-2 rounded-lg max-w-md ${msg.sender === "user" ? "bg-gray-900 text-white self-end ml-auto" : "bg-gray-200 text-black self-start"}`}>
              {msg.text}
            </div>
          ))}
        </CardContent>
        <div className="flex p-4 space-x-2 text-gray-800">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask Tourlanka..."
            className="flex-1"
          />
          <Button onClick={sendMessage}>
            <Send color="#ffffff" />
          </Button>
        </div>
      </Card>
    </div>
  );
}


