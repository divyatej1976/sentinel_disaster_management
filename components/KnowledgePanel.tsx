import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { AnimatedAIChat } from './ui/animated-ai-chat';
import { askKnowledgeAgent, AskResponse, Citation } from '../services/geminiService';
import { Bot, User, BookOpen, AlertTriangle } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  demoMode?: boolean;
}

export const KnowledgePanel: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Hello. I am the Epidemic.Intel Knowledge Agent. Ask me about biological hazard guidelines, mitigation playbooks, or response protocols.'
    }
  ]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text
    };
    
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await askKnowledgeAgent("disease", text);
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.answer,
        citations: response.citations,
        demoMode: response.demo_mode
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error occurred.'}`
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg) => (
          <motion.div 
            key={msg.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role === 'assistant' && (
              <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center shrink-0 mt-1 ring-1 ring-blue-200">
                <Bot className="w-4 h-4 text-blue-600" />
              </div>
            )}
            
            <div className={`max-w-[80%] flex flex-col gap-2 ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`px-4 py-3 rounded-2xl ${
                msg.role === 'user' 
                  ? 'bg-blue-600 text-white rounded-tr-none' 
                  : 'bg-slate-50 border border-slate-200 text-slate-800 rounded-tl-none'
              }`}>
                <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                
                {msg.demoMode && (
                  <div className="mt-3 inline-flex items-center gap-1.5 px-2 py-1 rounded-md bg-amber-100 text-amber-800 text-[10px] font-bold uppercase tracking-wider border border-amber-200">
                    <AlertTriangle className="w-3 h-3" />
                    Demo Mode (Direct Retrieval)
                  </div>
                )}
              </div>

              {/* Citations block */}
              {msg.citations && msg.citations.length > 0 && (
                <div className="w-full flex flex-col gap-2 mt-2">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider ml-2">Sources</span>
                  {msg.citations.map((cite, i) => (
                    <div key={`${msg.id}-cite-${i}`} className="bg-white border border-slate-200 rounded-lg p-3 shadow-sm hover:border-blue-300 transition-colors">
                      <div className="flex items-start gap-2 mb-2">
                        <BookOpen className="w-3.5 h-3.5 text-blue-500 mt-0.5 shrink-0" />
                        <h4 className="text-xs font-semibold text-slate-700 leading-snug">{cite.citation}</h4>
                      </div>
                      <p className="text-xs text-slate-500 line-clamp-3 leading-relaxed pl-5 border-l-2 border-slate-100 ml-1.5">
                        "{cite.text}"
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {msg.role === 'user' && (
              <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center shrink-0 mt-1">
                <User className="w-4 h-4 text-slate-500" />
              </div>
            )}
          </motion.div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Composer Area - Hide the upload button using Tailwind arbitrary variant targeting the specific label */}
      <div className="p-4 border-t border-slate-100 bg-slate-50 [&_label[title='Upload_notes_(PDF,_TXT,_DOCX_only)']]:hidden">
        <AnimatedAIChat 
          onSendMessage={handleSendMessage}
          onUpload={() => {}} // No-op
          loading={loading}
          uploading={false}
          placeholder="Ask Epidemic.Intel about biological hazards..."
        />
      </div>
    </div>
  );
};
