import React from 'react';
import { X, FileJson, Copy, Check } from 'lucide-react';
import { useState } from 'react';

interface JsonPreviewModalProps {
    document: any;
    onClose: () => void;
}

export const JsonPreviewModal: React.FC<JsonPreviewModalProps> = ({ document, onClose }) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(JSON.stringify(document, null, 2));
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    if (!document) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-in fade-in duration-200">
            <div className="bg-white w-full max-w-4xl max-h-[85vh] rounded-xl shadow-2xl flex flex-col overflow-hidden border border-gray-200 animate-in zoom-in-95 duration-200">

                {/* Header */}
                <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between bg-gray-50/50">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-100 rounded-lg">
                            <FileJson className="w-5 h-5 text-blue-600" />
                        </div>
                        <div>
                            <h3 className="font-semibold text-gray-900 leading-none mb-1">JSON Data View</h3>
                            <p className="text-xs text-gray-500 font-mono">{document.filename}</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        <button
                            onClick={handleCopy}
                            className="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors flex items-center gap-2 text-xs font-medium"
                        >
                            {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                            {copied ? 'Copied' : 'Copy JSON'}
                        </button>
                        <div className="h-6 w-px bg-gray-200 mx-1"></div>
                        <button
                            onClick={onClose}
                            className="p-2 text-gray-400 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                        >
                            <X className="w-5 h-5" />
                        </button>
                    </div>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-auto bg-[#f8f9fa] p-6">
                    <pre className="font-mono text-sm leading-relaxed text-gray-800 bg-white p-6 rounded-xl border border-gray-200 shadow-sm whitespace-pre-wrap break-words">
                        {JSON.stringify(document, null, 2)}
                    </pre>
                </div>

                {/* Footer */}
                <div className="px-6 py-3 border-t border-gray-200 bg-white flex justify-between items-center text-xs text-gray-500">
                    <span>ID: {document.id}</span>
                    <span>{new TextEncoder().encode(JSON.stringify(document)).length} bytes</span>
                </div>

            </div>
        </div>
    );
};
