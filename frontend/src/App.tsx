import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

// Get API URL from environment variable or use default
const API_URL = import.meta.env.VITE_API_URL || '';
axios.defaults.timeout = 10000;
// Set baseURL - if empty, axios will use relative URLs (which won't work in production)
// So we need to ensure API_URL is always set for production
if (API_URL) {
  axios.defaults.baseURL = API_URL;
} else {
  // Fallback: try to detect if we're in production and log error
  console.warn('VITE_API_URL is not set! Backend connection will fail.');
  // In production, we need the full URL
  axios.defaults.baseURL = '';
}

function App() {
  const [tab, setTab] = useState('voice');
  const [command, setCommand] = useState('');
  const [result, setResult] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [devices] = useState(['living room light', 'bedroom light', 'kitchen light', 'thermostat', 'fan', 'door lock']);
  const [deviceStates, setDeviceStates] = useState<Record<string, any>>({});
  const [isListening, setIsListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [interimTranscript, setInterimTranscript] = useState('');
  const [finalTranscript, setFinalTranscript] = useState('');
  const [audioLevel, setAudioLevel] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);
  const [recognitionError, setRecognitionError] = useState<string | null>(null);
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    const savedTheme = localStorage.getItem('theme');
    return (savedTheme === 'light' || savedTheme === 'dark') ? savedTheme : 'dark';
  });
  const recognitionRef = useRef<any>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const animationFrameRef = useRef<number | null>(null);

  useEffect(() => {
    // Apply theme to document
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  useEffect(() => {
    checkBackendStatus();
    loadHistory();
    loadDeviceStates();
    const interval = setInterval(() => {
      checkBackendStatus();
      loadDeviceStates();
    }, 5000);
    return () => {
      clearInterval(interval);
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, []);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const loadDeviceStates = async () => {
    try {
      const res = await axios.get('/api/devices');
      if (res.data?.states) {
        setDeviceStates(res.data.states);
      }
    } catch (e) {
      console.error('Failed to load device states:', e);
    }
  };

  const checkBackendStatus = async () => {
    try {
      const res = await axios.get('/api/health', { timeout: 3000 });
      if (res.data?.status === 'UP') {
        setBackendStatus('online');
      } else {
        setBackendStatus('offline');
      }
    } catch (e) {
      try {
        await axios.get('/api/devices', { timeout: 2000 });
        setBackendStatus('online');
      } catch (e2) {
        setBackendStatus('offline');
      }
    }
  };

  const loadHistory = async () => {
    try {
      const res = await axios.get('/api/history');
      setHistory(res.data || []);
    } catch (e) {
      console.error('Failed to load history:', e);
    }
  };

  const startAudioVisualization = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const analyser = audioContext.createAnalyser();
      const microphone = audioContext.createMediaStreamSource(stream);
      
      analyser.fftSize = 256;
      analyser.smoothingTimeConstant = 0.8;
      microphone.connect(analyser);
      
      audioContextRef.current = audioContext;
      analyserRef.current = analyser;
      
      const dataArray = new Uint8Array(analyser.frequencyBinCount);
      
      const updateAudioLevel = () => {
        if (!analyserRef.current) return;
        
        analyserRef.current.getByteFrequencyData(dataArray);
        const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
        const normalizedLevel = Math.min(average / 128, 1);
        setAudioLevel(normalizedLevel);
        
        if (isListening) {
          animationFrameRef.current = requestAnimationFrame(updateAudioLevel);
        }
      };
      
      updateAudioLevel();
    } catch (e) {
      console.warn('Audio visualization not available:', e);
    }
  };

  const stopAudioVisualization = () => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
    setAudioLevel(0);
  };

  const handleVoice = async () => {
    if (backendStatus !== 'online') {
      setError('Backend server is not available. Please wait for it to start.');
      return;
    }

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setError('Your browser does not support voice recognition. Please use Chrome, Edge, or Safari.');
      return;
    }

    if (isListening && recognitionRef.current) {
      recognitionRef.current.stop();
      stopAudioVisualization();
      setIsListening(false);
      setLoading(false);
      return;
    }

    setIsListening(true);
    setLoading(true);
    setResult(null);
    setError(null);
    setRecognitionError(null);
    setCommand('');
    setInterimTranscript('');
    setFinalTranscript('');
    setAudioLevel(0);

    try {
      await startAudioVisualization();
    } catch (e) {
      console.warn('Could not start audio visualization');
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    recognition.maxAlternatives = 3;
    recognitionRef.current = recognition;

    let timeoutId: NodeJS.Timeout;
    const resetTimeout = () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        if (isListening && !finalTranscript) {
          setRecognitionError('No speech detected. Please try again.');
          recognition.stop();
        }
      }, 5000);
    };

    recognition.onstart = () => {
      setLoading(false);
      resetTimeout();
    };

    recognition.onresult = (event: any) => {
      resetTimeout();
      let interim = '';
      let final = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i];
        const transcript = result[0].transcript.trim();
        
        if (result.isFinal) {
          final += transcript + ' ';
        } else {
          interim += transcript;
        }
      }

      if (interim) {
        setInterimTranscript(interim);
        setCommand((finalTranscript + ' ' + interim).trim());
      }

      if (final) {
        const newFinal = (finalTranscript + ' ' + final).trim();
        setFinalTranscript(newFinal);
        setInterimTranscript('');
        setCommand(newFinal);
        clearTimeout(timeoutId);

        if (newFinal.length > 0) {
          recognition.stop();
          stopAudioVisualization();
          setIsProcessing(true);
          setTimeout(() => {
            processCommand(newFinal).catch((e: any) => {
              setError(e.message || 'Failed to process command');
              setIsProcessing(false);
            });
          }, 300);
        }
      }
    };

    recognition.onerror = (event: any) => {
      clearTimeout(timeoutId);
      stopAudioVisualization();
      setIsListening(false);
      setLoading(false);
      setIsProcessing(false);
      recognitionRef.current = null;

      let errorMsg = '';
      let userFriendlyMsg = '';
      
      switch (event.error) {
        case 'no-speech':
          errorMsg = 'No speech detected. Please speak clearly.';
          userFriendlyMsg = 'No speech detected. Try speaking louder or closer to your microphone.';
          break;
        case 'audio-capture':
          errorMsg = 'No microphone found.';
          userFriendlyMsg = 'No microphone detected. Please connect a microphone and try again.';
          break;
        case 'not-allowed':
          errorMsg = 'Microphone permission denied.';
          userFriendlyMsg = 'Microphone access denied. Please allow microphone permissions in your browser settings.';
          break;
        case 'network':
          errorMsg = 'Network error occurred.';
          userFriendlyMsg = 'Network error. Please check your internet connection.';
          break;
        case 'aborted':
          errorMsg = 'Recognition aborted.';
          userFriendlyMsg = 'Voice recognition was stopped.';
          break;
        case 'service-not-allowed':
          errorMsg = 'Speech recognition service not allowed.';
          userFriendlyMsg = 'Speech recognition service is not available.';
          break;
        default:
          errorMsg = `Recognition error: ${event.error || 'Unknown error'}`;
          userFriendlyMsg = 'An error occurred during voice recognition. Please try again.';
      }
      
      setRecognitionError(errorMsg);
      setError(userFriendlyMsg);
    };

    recognition.onend = () => {
      clearTimeout(timeoutId);
      stopAudioVisualization();
      const fullCommand = (finalTranscript + ' ' + interimTranscript).trim();
      
      if (fullCommand.length > 0 && !isProcessing && !loading) {
        setIsProcessing(true);
        processCommand(fullCommand).catch((e: any) => {
          setError(e.message || 'Failed to process command');
          setIsProcessing(false);
        });
      } else if (!isProcessing && !loading) {
        setIsListening(false);
        setLoading(false);
        setInterimTranscript('');
        setFinalTranscript('');
      }
      recognitionRef.current = null;
    };

    try {
      recognition.start();
    } catch (e: any) {
      stopAudioVisualization();
      setError('Failed to start voice recognition. Please try again.');
      setIsListening(false);
      setLoading(false);
    }
  };

  const processCommand = async (commandText: string) => {
    if (!commandText?.trim()) {
      setIsListening(false);
      setLoading(false);
      setIsProcessing(false);
      throw new Error('No command detected.');
    }

    setLoading(true);
    setIsListening(false);
    setIsProcessing(true);
    setError(null); // Clear any previous errors

    try {
      const res = await axios.post('/api/interpret', { command: commandText }, {
        timeout: 10000,
        validateStatus: (status) => status < 500
      });

      if (res.data.success === false) {
        throw new Error(res.data.error || 'Failed to interpret command');
      }

      if (!res.data.command?.device) {
        throw new Error('Invalid response from server');
      }

      const executeRes = await axios.post('/api/execute', res.data.command, {
        timeout: 10000,
        validateStatus: (status) => status < 500
      });

      if (executeRes.data.success === false) {
        setError(`Execution failed: ${executeRes.data.message || 'Unknown error'}`);
        setResult(null); // Clear result on execution failure
      } else {
        // Set result after successful execution
        setResult({
          ...res.data,
          executed: true,
          deviceState: executeRes.data.deviceState
        });
        
        if (executeRes.data.deviceState && res.data.command?.device) {
          setDeviceStates(prev => ({
            ...prev,
            [res.data.command.device]: executeRes.data.deviceState
          }));
        }
      }

      loadHistory();
      loadDeviceStates();
    } catch (e: any) {
      let errorMessage = 'Failed to process command.';
      if (e.response?.data?.error) {
        errorMessage = e.response.data.error;
      } else if (e.message) {
        errorMessage = e.message;
      }
      setError(errorMessage);
      setResult(null); // Clear result on error
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
      setIsProcessing(false);
    }
  };

  const handleBuild = async () => {
    const trimmedCommand = command.trim();
    if (!trimmedCommand) {
      setError('Please enter a command');
      return;
    }

    if (backendStatus !== 'online') {
      setError('Backend server is not available.');
      return;
    }

    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const res = await axios.post('/api/interpret', { command: trimmedCommand }, {
        timeout: 10000,
        validateStatus: (status) => status < 500
      });

      if (res.data.success === false) {
        throw new Error(res.data.error || 'Failed to interpret command');
      }

      setResult(res.data);

      const executeRes = await axios.post('/api/execute', res.data.command, {
        timeout: 10000,
        validateStatus: (status) => status < 500
      });

      if (executeRes.data.success === false) {
        setError(`Execution failed: ${executeRes.data.message || 'Unknown error'}`);
      } else {
        if (executeRes.data.deviceState && res.data.command?.device) {
          setDeviceStates(prev => ({
            ...prev,
            [res.data.command.device]: executeRes.data.deviceState
          }));
        }
        setCommand('');
      }

      loadHistory();
      loadDeviceStates();
    } catch (e: any) {
      let errorMessage = 'Failed to process command.';
      if (e.response?.data?.error) {
        errorMessage = e.response.data.error;
      } else if (e.message) {
        errorMessage = e.message;
      }
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="app-container">
        <header className="app-header">
          <div className="header-content">
            <div className="logo-section">
              <div className="logo-icon">🎙️</div>
              <div className="logo-text">
                <h1>Voice Automation Hub</h1>
                <p className="subtitle">AI-Powered Smart Home Control</p>
              </div>
            </div>
            <div className="header-actions">
              <button 
                className="theme-toggle"
                onClick={toggleTheme}
                title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
                aria-label="Toggle theme"
              >
                {theme === 'dark' ? '☀️' : '🌙'}
              </button>
              <div className={`status-indicator ${backendStatus}`}>
                <span className="status-dot"></span>
                <span className="status-text">
                  {backendStatus === 'online' ? 'Connected' : backendStatus === 'offline' ? 'Disconnected' : 'Connecting...'}
                </span>
              </div>
            </div>
          </div>
        </header>

        <nav className="main-nav">
          <button 
            className={`nav-item ${tab === 'voice' ? 'active' : ''}`} 
            onClick={() => { setTab('voice'); setResult(null); setError(null); }}
          >
            <span className="nav-icon">🎤</span>
            <span className="nav-label">Voice</span>
          </button>
          <button 
            className={`nav-item ${tab === 'builder' ? 'active' : ''}`} 
            onClick={() => { setTab('builder'); setResult(null); setError(null); }}
          >
            <span className="nav-icon">⌨️</span>
            <span className="nav-label">Text</span>
          </button>
          <button 
            className={`nav-item ${tab === 'devices' ? 'active' : ''}`} 
            onClick={() => setTab('devices')}
          >
            <span className="nav-icon">🏠</span>
            <span className="nav-label">Devices</span>
          </button>
          <button 
            className={`nav-item ${tab === 'history' ? 'active' : ''}`} 
            onClick={() => { setTab('history'); loadHistory(); }}
          >
            <span className="nav-icon">📋</span>
            <span className="nav-label">History</span>
            {history.length > 0 && <span className="nav-badge">{history.length}</span>}
          </button>
        </nav>

        <main className="main-content">
          {tab === 'voice' && (
            <div className="voice-panel">
              <div className="panel-header">
                <h2>Voice Command</h2>
                <p>Speak naturally to control your devices</p>
              </div>

              <div className="voice-control-area">
                <div className="voice-button-wrapper">
                  <button 
                    className={`voice-button ${isListening ? 'listening' : ''} ${isProcessing || loading ? 'processing' : ''}`}
                    onClick={handleVoice}
                    disabled={(isProcessing || loading) && !isListening || backendStatus !== 'online'}
                    title={backendStatus !== 'online' ? 'Waiting for server connection...' : isListening ? 'Click to stop listening' : isProcessing ? 'Processing command...' : 'Click to start voice command'}
                  >
                    {isProcessing || loading ? (
                      <>
                        <span className="button-icon">⏳</span>
                        <span>Processing Command...</span>
                      </>
                    ) : isListening ? (
                      <>
                        <span className="button-icon pulse">🎤</span>
                        <span>Listening... Speak Now</span>
                      </>
                    ) : (
                      <>
                        <span className="button-icon">🎙️</span>
                        <span>Start Voice Command</span>
                      </>
                    )}
                  </button>
                  
                  {isListening && (
                    <div className="audio-waveform">
                      {Array.from({ length: 20 }).map((_, i) => (
                        <div
                          key={i}
                          className="waveform-bar"
                          style={{
                            height: `${20 + (audioLevel * 80) * Math.sin(i * 0.5 + Date.now() * 0.01)}%`,
                            animationDelay: `${i * 0.05}s`
                          }}
                        />
                      ))}
                    </div>
                  )}
                </div>
                
                {!isListening && !loading && !isProcessing && (
                  <p className="help-text">Click the button above and speak your command naturally</p>
                )}
                
                {recognitionError && (
                  <div className="recognition-error">
                    <span className="error-icon-small">⚠️</span>
                    <span>{recognitionError}</span>
                  </div>
                )}
              </div>

              {(isListening || finalTranscript || interimTranscript) && (
                <div className="transcription-box">
                  <div className="transcription-header">
                    <span className="transcription-label">Live Transcription</span>
                    {isListening && <span className="live-indicator"></span>}
                    {isProcessing && <span className="processing-badge">Processing...</span>}
                  </div>
                  <div className="transcription-content">
                    {finalTranscript && (
                      <div className="transcript-line">
                        <span className="final-text">{finalTranscript}</span>
                      </div>
                    )}
                    {interimTranscript && (
                      <div className="transcript-line">
                        <span className="interim-text">{interimTranscript}</span>
                        <span className="typing-cursor">|</span>
                      </div>
                    )}
                    {!finalTranscript && !interimTranscript && (
                      <span className="placeholder">Speak your command clearly...</span>
                    )}
                  </div>
                  {finalTranscript && (
                    <div className="transcription-footer">
                      <span className="transcript-hint">Command detected. Processing...</span>
                    </div>
                  )}
                </div>
              )}

              {error && (
                <div className="error-box">
                  <span className="error-icon">⚠️</span>
                  <span className="error-message">{error}</span>
                </div>
              )}

              {result && (
                <div className="result-box">
                  <div className="result-header">
                    <span className="result-icon">✅</span>
                    <span>Command Executed</span>
                  </div>
                  <div className="result-details">
                    <div className="result-item">
                      <span className="result-label">Device:</span>
                      <span className="result-value device">{result.command?.device}</span>
                    </div>
                    <div className="result-item">
                      <span className="result-label">Action:</span>
                      <span className="result-value action">{result.command?.action}</span>
                    </div>
                    {result.command?.parameter && (
                      <div className="result-item">
                        <span className="result-label">Value:</span>
                        <span className="result-value">{result.command.parameter}</span>
                      </div>
                    )}
                  </div>
                  {result.confidence && (
                    <div className="confidence-indicator">
                      <span className="confidence-label">Confidence:</span>
                      <div className="confidence-bar">
                        <div 
                          className="confidence-fill" 
                          style={{ width: `${result.confidence * 100}%` }}
                        >
                          {Math.round(result.confidence * 100)}%
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {tab === 'builder' && (
            <div className="builder-panel">
              <div className="panel-header">
                <h2>Text Command</h2>
                <p>Type your command in natural language</p>
              </div>

              <div className="input-group">
                <input
                  type="text"
                  className="command-input"
                  placeholder="e.g., Turn on the living room light"
                  value={command}
                  onChange={(e) => setCommand(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !loading && command.trim() && handleBuild()}
                  disabled={loading || backendStatus !== 'online'}
                  title="Type your command in natural language"
                />
                <button 
                  className="execute-button"
                  onClick={handleBuild}
                  disabled={loading || !command.trim() || backendStatus !== 'online'}
                  title={!command.trim() ? 'Enter a command first' : backendStatus !== 'online' ? 'Waiting for server...' : 'Execute command'}
                >
                  {loading ? 'Processing...' : 'Execute'}
                </button>
              </div>
              <div className="example-hints">
                <p className="hint-label">Try these examples:</p>
                <div className="example-chips">
                  <button 
                    className="example-chip"
                    onClick={() => setCommand('Turn on the living room light')}
                    disabled={loading || backendStatus !== 'online'}
                  >
                    Turn on the living room light
                  </button>
                  <button 
                    className="example-chip"
                    onClick={() => setCommand('Set thermostat to 72')}
                    disabled={loading || backendStatus !== 'online'}
                  >
                    Set thermostat to 72
                  </button>
                  <button 
                    className="example-chip"
                    onClick={() => setCommand('Dim the bedroom light')}
                    disabled={loading || backendStatus !== 'online'}
                  >
                    Dim the bedroom light
                  </button>
                </div>
              </div>

              {error && (
                <div className="error-box">
                  <span className="error-icon">⚠️</span>
                  <span className="error-message">{error}</span>
                </div>
              )}

              {result && (
                <div className="result-box">
                  <div className="result-header">
                    <span className="result-icon">✅</span>
                    <span>Command Executed</span>
                  </div>
                  <div className="result-details">
                    <div className="result-item">
                      <span className="result-label">Device:</span>
                      <span className="result-value device">{result.command?.device}</span>
                    </div>
                    <div className="result-item">
                      <span className="result-label">Action:</span>
                      <span className="result-value action">{result.command?.action}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {tab === 'devices' && (
            <div className="devices-panel">
              <div className="panel-header">
                <h2>Device Control</h2>
                <p>Monitor and control all your smart devices</p>
              </div>

              <div className="devices-grid">
                {devices.map((device, i) => {
                  const state = deviceStates[device] || { isOn: false, status: 'OFF' };
                  const isOn = state.isOn || state.status === 'ON';

                  return (
                    <div key={i} className={`device-card ${isOn ? 'active' : ''}`}>
                      <div className="device-header">
                        <div className="device-icon">
                          {device.includes('light') ? '💡' : 
                           device.includes('thermostat') ? '🌡️' : 
                           device.includes('fan') ? '🌀' : 
                           device.includes('door') ? '🔒' : '📱'}
                        </div>
                        <div className={`device-status ${isOn ? 'on' : 'off'}`}>
                          {isOn ? 'ON' : 'OFF'}
                        </div>
                      </div>
                      <div className="device-name">{device}</div>
                      
                      {device.includes('light') && state.brightness !== undefined && (
                        <div className="device-metric">
                          <span className="metric-label">Brightness</span>
                          <div className="metric-bar">
                            <div 
                              className="metric-fill" 
                              style={{ width: `${state.brightness}%` }}
                            >
                              {state.brightness}%
                            </div>
                          </div>
                        </div>
                      )}
                      
                      {device === 'thermostat' && state.temperature !== undefined && (
                        <div className="device-metric">
                          <span className="metric-value">{state.temperature}°F</span>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {tab === 'history' && (
            <div className="history-panel">
              <div className="panel-header">
                <h2>Command History</h2>
                <p>View all executed commands</p>
              </div>

              {history.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-icon">📭</div>
                  <h3>No Commands Yet</h3>
                  <p>Start using voice or text commands to see history</p>
                </div>
              ) : (
                <div className="history-list">
                  {history.map((h, i) => (
                    <div key={i} className="history-item">
                      <div className="history-icon">⚡</div>
                      <div className="history-content">
                        <div className="history-command">
                          <span className="history-device">{h.device}</span>
                          <span className="history-arrow">→</span>
                          <span className="history-action">{h.action}</span>
                          {h.parameter && (
                            <>
                              <span className="history-separator">:</span>
                              <span className="history-parameter">{h.parameter}</span>
                            </>
                          )}
                        </div>
                        {h.timestamp && (
                          <div className="history-time">
                            {new Date(h.timestamp).toLocaleString()}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
