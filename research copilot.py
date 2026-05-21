import React, { useState } from 'react';

interface Message {
  role: string;
  content: string;
}

const agents = [
  'Coordinator Agent',
  'Literature Agent',
  'Method Agent',
  'Data Agent',
  'Code Agent',
  'Writing Agent'
];

export default function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      role: 'User',
      content: input
    };

    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: input
        })
      });

      const data = await response.json();

      setMessages(prev => [
        ...prev,
        {
          role: 'AI Research Copilot',
          content: data.response
        }
      ]);

    } catch (error) {
      setMessages(prev => [
        ...prev,
        {
          role: 'System',
          content: '服务器连接失败'
        }
      ]);
    }

    setLoading(false);
    setInput('');
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-5xl mx-auto bg-white rounded-2xl shadow-lg p-6">

        <h1 className="text-4xl font-bold mb-6 text-center">
          AI Research Copilot
        </h1>

        <div className="grid grid-cols-3 gap-4 mb-6">
          {agents.map(agent => (
            <div
              key={agent}
              className="bg-blue-100 p-4 rounded-xl text-center font-semibold"
            >
              {agent}
            </div>
          ))}
        </div>

        <div className="h-[500px] overflow-y-auto border rounded-xl p-4 mb-4 bg-gray-50">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`mb-4 p-4 rounded-xl ${
                msg.role === 'User'
                  ? 'bg-blue-500 text-white ml-20'
                  : 'bg-white border mr-20'
              }`}
            >
              <div className="font-bold mb-2">
                {msg.role}
              </div>
              <div>
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="bg-yellow-100 p-4 rounded-xl">
              多Agent正在协同推理中...
            </div>
          )}
        </div>

        <div className="flex gap-4">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="请输入研究任务..."
            className="flex-1 border rounded-xl p-4"
          />

          <button
            onClick={sendMessage}
            className="bg-blue-600 text-white px-6 py-4 rounded-xl"
          >
            发送
          </button>
        </div>
      </div>
    </div>
  );
}

