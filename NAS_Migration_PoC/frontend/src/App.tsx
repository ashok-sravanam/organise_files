import { useState, useEffect } from 'react';
import { Login } from './components/Login';
import { JsonPreviewModal } from './components/JsonPreviewModal';
import { useWebSocket } from './hooks/useWebSocket';
import { Search, FileText, FolderOpen, Activity, Briefcase, GraduationCap, Code, DollarSign, Home, ChevronRight, FileJson } from 'lucide-react';
import Fuse from 'fuse.js';

interface Document {
  id: number;
  filename: string;
  category: string;
  subfolder: string;
  extracted_text_preview: string;
  confidence: number;
  file_type: string;
  [key: string]: any; // Allow other fields for JSON view
}

const CATEGORIES = [
  { id: 'all', label: 'All Files', icon: Home, color: 'text-blue-500' },
  { id: 'Career', label: 'Career', icon: Briefcase, color: 'text-purple-500' },
  { id: 'Academic', label: 'Academic', icon: GraduationCap, color: 'text-green-500' },
  { id: 'Projects', label: 'Projects', icon: Code, color: 'text-orange-500' },
  { id: 'Financial', label: 'Financial', icon: DollarSign, color: 'text-red-500' },
];

function App() {
  const [token, setToken] = useState<string | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [query, setQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('all');
  const [results, setResults] = useState<Document[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);

  const { isConnected } = useWebSocket(token, (data) => {
    if (Array.isArray(data)) setDocuments(data);
  });

  useEffect(() => {
    if (token) {
      fetch('http://127.0.0.1:8000/documents', {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(data => setDocuments(data))
        .catch(err => console.error(err));
    }
  }, [token]);

  useEffect(() => {
    let filtered = documents;

    if (activeCategory !== 'all') {
      filtered = filtered.filter(d => d.category === activeCategory);
    }

    if (query) {
      const fuse = new Fuse(filtered, {
        keys: ['filename', 'extracted_text', 'category', 'tags'],
        threshold: 0.3
      });
      setResults(fuse.search(query).map(res => res.item));
    } else {
      setResults(filtered);
    }
  }, [query, documents, activeCategory]);

  if (!token) return <Login onLogin={setToken} />;

  const categoryData = CATEGORIES.map(cat => ({
    ...cat,
    count: cat.id === 'all' ? documents.length : documents.filter(d => d.category === cat.id).length
  }));

  return (
    <div className="h-screen flex flex-col bg-[#f5f5f7] p-3 text-gray-900 font-sans">

      {selectedDoc && (
        <JsonPreviewModal
          document={selectedDoc}
          onClose={() => setSelectedDoc(null)}
        />
      )}

      {/* macOS-style Window */}
      <div className="macos-window h-full flex overflow-hidden">

        {/* Sidebar */}
        <aside className="w-52 macos-sidebar flex flex-col p-2">

          {/* Sidebar Header */}
          <div className="px-3 py-3 mb-2 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500 border border-red-600/20"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500 border border-yellow-600/20"></div>
              <div className="w-3 h-3 rounded-full bg-green-500 border border-green-600/20"></div>
            </div>
          </div>

          <div className="px-3 mb-4">
            <h1 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Favorites</h1>
            <div className={`flex items-center gap-2 text-xs font-medium py-1 ${isConnected ? 'text-green-600' : 'text-red-400'}`}>
              <Activity size={12} />
              {isConnected ? 'Sync Active' : 'Offline'}
            </div>
          </div>

          {/* Categories */}
          <nav className="flex-1 space-y-0.5">
            {categoryData.map(cat => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`macos-sidebar-item w-full ${activeCategory === cat.id ? 'macos-sidebar-item-active' : ''}`}
              >
                <cat.icon className={`w-4 h-4 ${cat.color} opacity-90`} />
                <span className="flex-1 text-left">{cat.label}</span>
                {cat.count > 0 && <span className="text-[10px] text-gray-400 font-medium bg-gray-200/50 px-1.5 py-0.5 rounded-full">{cat.count}</span>}
              </button>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 flex flex-col bg-white">

          {/* Toolbar */}
          <header className="h-14 border-b border-gray-200 flex items-center justify-between px-4 bg-white/80 backdrop-blur-md sticky top-0 z-10">

            {/* Breadcrumb / Nav */}
            <div className="flex items-center gap-2">
              <button className="p-1.5 hover:bg-gray-100 rounded-md text-gray-400">
                <ChevronRight className="w-5 h-5 rotate-180" />
              </button>
              <button className="p-1.5 hover:bg-gray-100 rounded-md text-gray-400">
                <ChevronRight className="w-5 h-5" />
              </button>
              <div className="h-6 w-px bg-gray-200 mx-2"></div>
              <span className="font-semibold text-lg text-gray-800">{activeCategory === 'all' ? 'All Files' : activeCategory}</span>
            </div>

            {/* Search */}
            <div className="w-64">
              <div className="relative group">
                <Search className="absolute left-2.5 top-1.5 w-4 h-4 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
                <input
                  type="text"
                  placeholder="Search"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="macos-searchbar pl-8 transition-all"
                />
              </div>
            </div>
          </header>

          {/* File List */}
          <div className="flex-1 overflow-y-auto p-4 bg-white">
            <div className="grid grid-cols-1 gap-0">
              {results.map((doc, index) => {
                const Icon = doc.category === 'Career' ? Briefcase :
                  doc.category === 'Academic' ? GraduationCap :
                    doc.category === 'Projects' ? Code :
                      doc.category === 'Financial' ? DollarSign : FileText;

                const iconColor = doc.category === 'Career' ? 'text-purple-600' :
                  doc.category === 'Academic' ? 'text-green-600' :
                    doc.category === 'Projects' ? 'text-orange-500' :
                      doc.category === 'Financial' ? 'text-red-500' : 'text-blue-500';

                return (
                  <div
                    key={doc.id}
                    onClick={() => setSelectedDoc(doc)}
                    className={`group flex items-center gap-4 p-3 border-b border-gray-50 hover:bg-[#f0f2f5] cursor-default transition-colors ${index === 0 ? 'border-t-0' : ''}`}
                  >

                    {/* File Icon */}
                    <div className="w-10 h-10 flex items-center justify-center">
                      <Icon className={`w-8 h-8 ${iconColor} opacity-90`} strokeWidth={1.5} />
                    </div>

                    {/* File Info */}
                    <div className="flex-1 min-w-0">
                      <h3 className="font-medium text-sm text-gray-900 truncate mb-0.5">{doc.filename}</h3>
                      <div className="flex items-center gap-2 text-xs text-gray-500">
                        <span>{doc.file_type}</span>
                        <span className="text-gray-300">•</span>
                        <span>{new Date().toLocaleDateString()}</span>
                        <span className="text-gray-300">•</span>
                        <span className="flex items-center gap-1">
                          {Math.round(doc.confidence)}% match
                        </span>
                      </div>
                    </div>

                    {/* Quick Badge */}
                    <div className="px-2.5 py-1 rounded-full text-[10px] font-medium bg-gray-100 text-gray-500 group-hover:bg-white group-hover:shadow-sm transition-all uppercase tracking-wide">
                      {doc.category}
                    </div>

                    {/* Action Icon */}
                    <button className="p-2 text-gray-300 hover:text-blue-500 transition-colors">
                      <FileJson className="w-4 h-4" />
                    </button>

                  </div>
                );
              })}
            </div>

            {results.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-gray-400 pb-20">
                <Search className="w-12 h-12 mb-3 opacity-20" />
                <p className="text-sm font-medium">No items found</p>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
