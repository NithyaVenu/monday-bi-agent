// // import { useState } from "react"
// import { useState, useEffect, useRef } from "react"
// import axios from "axios"


// const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

// type Message = { role: "user" | "assistant"; content: string; trace?: any[] }

// export default function App() {

//   const [messages, setMessages] = useState<Message[]>([])
//   const [input, setInput] = useState("")
//   const [loading, setLoading] = useState(false)
//   const [showTrace, setShowTrace] = useState<any[] | null>(null)
//   const messagesEndRef = useRef<HTMLDivElement>(null)

//   useEffect(() => {
//   messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
// }, [messages, loading])

//   const sendMessage = async () => {
//     if (!input.trim()) return
//     const userMsg: Message = { role: "user", content: input }
//     const updatedMessages = [...messages, userMsg]
//     setMessages(updatedMessages)
//     setInput("")
//     setLoading(true)

//     const history = updatedMessages.slice(0, -1).map(m => ({
//       role: m.role, content: m.content
//     }))

//     try {
//       const res = await axios.post(`${API_URL}/chat`, {
//         message: input,
//         history
//       })
//       const assistantMsg: Message = {
//         role: "assistant",
//         content: res.data.answer,
//         trace: res.data.trace
//       }
//       setMessages([...updatedMessages, assistantMsg])
//     } catch (e) {
//       setMessages([...updatedMessages, {
//         role: "assistant",
//         content: "Something went wrong. Please try again."
//       }])
//     }
//     setLoading(false)
//   }

//   return (
//     <div style={{
//       display: "flex",
//       height: "100vh",
//       width: "100vw",
//       background: "#f5f6fa",
//       justifyContent: "center",
//       alignItems: "stretch",
//       boxSizing: "border-box",
//       overflow: "hidden"
//     }}>

//       {/* Main Chat Container */}
//       <div style={{
//         display: "flex",
//         flexDirection: "column",
//         width: "100%",
//         maxWidth: "760px",
//         height: "100vh",
//         background: "#ffffff",
//         boxShadow: "0 0 30px rgba(0,0,0,0.08)",
//         boxSizing: "border-box",
//         overflow: "hidden"
//       }}>

//         {/* Header */}
//         <div style={{
//           padding: "18px 24px",
//           borderBottom: "1px solid #e9ecef",
//           background: "#ffffff",
//           flexShrink: 0
//         }}>
//           <h2 style={{ margin: 0, fontSize: "18px", fontWeight: 600, color: "#1a1a2e" }}>
//             🤖 Monday.com BI Agent
//           </h2>
//           <p style={{ margin: "4px 0 0", fontSize: "13px", color: "#888" }}>
//             Ask founder-level business questions
//           </p>
//         </div>

//         {/* Messages Area */}
//         <div style={{
//           flex: 1,
//           overflowY: "auto",
//           padding: "20px 24px",
//           display: "flex",
//           flexDirection: "column",
//           gap: "16px",
//           boxSizing: "border-box"
//         }}>
//           {messages.length === 0 && (
//             <div style={{
//               textAlign: "center",
//               color: "#aaa",
//               marginTop: "60px",
//               fontSize: "14px"
//             }}>
//               <div style={{ fontSize: "36px", marginBottom: "12px" }}>📊</div>
//               <div>Ask a business question to get started</div>
//               <div style={{ marginTop: "8px", fontSize: "13px", color: "#bbb" }}>
//                 e.g. "How's our pipeline looking this quarter?"
//               </div>
//             </div>
//           )}

//           {messages.map((m, i) => (
//             <div key={i} style={{
//               display: "flex",
//               flexDirection: "column",
//               alignItems: m.role === "user" ? "flex-end" : "flex-start",
//               width: "100%"
//             }}>
//               {/* Role label */}
//               <div style={{
//                 fontSize: "11px",
//                 color: "#aaa",
//                 marginBottom: "4px",
//                 paddingLeft: m.role === "user" ? "0" : "4px",
//                 paddingRight: m.role === "user" ? "4px" : "0"
//               }}>
//                 {m.role === "user" ? "You" : "BI Agent"}
//               </div>

//               {/* Message bubble */}
//               <div style={{
//                 padding: "12px 16px",
//                 borderRadius: m.role === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
//                 background: m.role === "user" ? "#0073ea" : "#f0f2f5",
//                 color: m.role === "user" ? "white" : "#1a1a2e",
//                 maxWidth: "80%",
//                 width: "fit-content",
//                 whiteSpace: "pre-wrap",
//                 wordBreak: "break-word",
//                 fontSize: "14px",
//                 lineHeight: "1.6",
//                 boxSizing: "border-box"
//               }}>
//                 {m.content}
//               </div>

//               {/* Trace button */}
//               {m.trace && m.trace.length > 0 && (
//                 <button
//                   onClick={() => setShowTrace(showTrace ? null : m.trace!)}
//                   style={{
//                     marginTop: "6px",
//                     fontSize: "12px",
//                     color: "#0073ea",
//                     background: "none",
//                     border: "1px solid #d0e8ff",
//                     borderRadius: "12px",
//                     padding: "3px 10px",
//                     cursor: "pointer",
//                     alignSelf: "flex-start"
//                   }}>
//                   🔍 {showTrace ? "Hide" : "View"} agent trace ({m.trace.length} calls)
//                 </button>
//               )}

//               {/* Inline Trace Panel */}
//               {m.trace && showTrace === m.trace && (
//                 <div style={{
//                   marginTop: "8px",
//                   background: "#fafafa",
//                   border: "1px solid #e9ecef",
//                   borderRadius: "12px",
//                   padding: "12px 16px",
//                   width: "100%",
//                   boxSizing: "border-box"
//                 }}>
//                   <div style={{ fontSize: "12px", fontWeight: 600, marginBottom: "8px", color: "#555" }}>
//                     Agent Trace
//                   </div>
//                   {showTrace.map((t, j) => (
//                     <div key={j} style={{
//                       background: "white",
//                       border: "1px solid #eee",
//                       borderRadius: "8px",
//                       padding: "8px 12px",
//                       marginBottom: "6px",
//                       fontSize: "13px"
//                     }}>
//                       <span style={{ fontWeight: 600 }}>🔧 {t.tool}</span>
//                       <span style={{ color: "#888", marginLeft: "10px" }}>Status: {t.status}</span>
//                       {t.records_returned !== undefined && (
//                         <span style={{ color: "#0073ea", marginLeft: "10px" }}>
//                           {t.records_returned} records
//                         </span>
//                       )}
//                     </div>
//                   ))}
//                 </div>
//               )}
//             </div>
//           ))}

//           {loading && (
//             <div style={{
//               display: "flex",
//               alignItems: "center",
//               gap: "8px",
//               color: "#888",
//               fontSize: "13px"
//             }}>
//               <div style={{
//                 width: "8px", height: "8px",
//                 borderRadius: "50%",
//                 background: "#0073ea",
//                 animation: "pulse 1s infinite"
//               }} />
//               Thinking...
//             </div>
//           )}

//         {/* Auto scroll anchor */}
//           <div ref={messagesEndRef} />

//         </div>

//         {/* Input Area */}
//         <div style={{
//           padding: "16px 24px",
//           borderTop: "1px solid #e9ecef",
//           background: "#ffffff",
//           flexShrink: 0,
//           boxSizing: "border-box"
//         }}>
//           <div style={{
//             display: "flex",
//             gap: "10px",
//             alignItems: "center"
//           }}>
//             <input
//               value={input}
//               onChange={e => setInput(e.target.value)}
//               onKeyDown={e => e.key === "Enter" && !e.shiftKey && sendMessage()}
//               placeholder="Ask a business question..."
//               style={{
//               flex: 1,
//               padding: "12px 16px",
//               borderRadius: "24px",
//               border: "1px solid #e0e0e0",
//               fontSize: "14px",
//               outline: "none",
//               background: "#f5f6fa",
//               boxSizing: "border-box",
//               color: "#1a1a2e",
//               caretColor: "#0073ea"
//             }}
//             />
//             <button
//               onClick={sendMessage}
//               disabled={loading}
//               style={{
//                 padding: "12px 20px",
//                 background: loading ? "#ccc" : "#0073ea",
//                 color: "white",
//                 border: "none",
//                 borderRadius: "24px",
//                 cursor: loading ? "not-allowed" : "pointer",
//                 fontSize: "14px",
//                 fontWeight: 600,
//                 flexShrink: 0
//               }}>
//               {loading ? "..." : "Send"}
//             </button>
//           </div>
//         </div>
//       </div>
//     </div>
//   )
// }
import { useState, useEffect, useRef } from "react"
import axios from "axios"

const API_URL = "https://monday-bi-agent-production-71a9.up.railway.app"

type Message = { role: "user" | "assistant"; content: string; trace?: any[] }

const SAMPLE_QUESTIONS = [
  {
    category: "Pipeline & Deals",
    icon: "💼",
    questions: [
      "How's our pipeline looking this quarter?",
      "Which deals are most likely to close soon?",
      "What's the total value of all open deals?",
      "Which client has the highest deal value?"
    ]
  },
  {
    category: "Sector Performance",
    icon: "📊",
    questions: [
      "Which sector has the most deals?",
      "Compare pipeline value across all sectors",
      "Show me all deals in the Mining sector",
      "How is the Renewables sector performing?"
    ]
  },
  {
    category: "Operations",
    icon: "⚙️",
    questions: [
      "How many work orders are currently active?",
      "Which work orders are overdue?",
      "What's the status of our current projects?",
      "Which work orders are linked to Railways sector?"
    ]
  },
  {
    category: "Cross-Board",
    icon: "🔀",
    questions: [
      "Which sectors have both active deals and work orders?",
      "Give me a full business summary",
      "Where are we most at risk right now?",
      "Give me a morning briefing on the business"
    ]
  }
]

export default function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [showTrace, setShowTrace] = useState<any[] | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, loading])

  const sendMessage = async (messageText?: string) => {
    const text = messageText || input
    if (!text.trim()) return

    const userMsg: Message = { role: "user", content: text }
    const updatedMessages = [...messages, userMsg]
    setMessages(updatedMessages)
    setInput("")
    setLoading(true)

    const history = updatedMessages.slice(0, -1).map(m => ({
      role: m.role, content: m.content
    }))

    try {
      const res = await axios.post(`${API_URL}/chat`, {
        message: text,
        history
      })
      const assistantMsg: Message = {
        role: "assistant",
        content: res.data.answer,
        trace: res.data.trace
      }
      setMessages([...updatedMessages, assistantMsg])
    } catch (e) {
      setMessages([...updatedMessages, {
        role: "assistant",
        content: "Something went wrong. Please try again."
      }])
    }
    setLoading(false)
  }

  const handleSampleClick = (question: string) => {
    setInput(question)
  }

  return (
    <div style={{
      display: "flex",
      height: "100vh",
      width: "100vw",
      background: "#f5f6fa",
      overflow: "hidden",
      fontFamily: "Arial, sans-serif",
      boxSizing: "border-box"
    }}>

      {/* Left Sidebar */}
      {sidebarOpen && (
        <div style={{
          width: "260px",
          minWidth: "260px",
          height: "100vh",
          background: "#ffffff",
          borderRight: "1px solid #e9ecef",
          display: "flex",
          flexDirection: "column",
          overflowY: "auto",
          boxSizing: "border-box"
        }}>
          {/* Sidebar Header */}
          <div style={{
            padding: "18px 16px 12px",
            borderBottom: "1px solid #e9ecef",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center"
          }}>
            <div>
              <div style={{ fontWeight: 700, fontSize: "13px", color: "#1a1a2e" }}>
                Sample Questions
              </div>
              <div style={{ fontSize: "11px", color: "#888", marginTop: "2px" }}>
                Click to ask
              </div>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              style={{
                background: "none", border: "none", cursor: "pointer",
                color: "#888", fontSize: "16px", padding: "2px 6px",
                borderRadius: "4px"
              }}>
              ✕
            </button>
          </div>

          {/* Question Categories */}
          <div style={{ padding: "12px 10px", flex: 1 }}>
            {SAMPLE_QUESTIONS.map((cat, ci) => (
              <div key={ci} style={{ marginBottom: "16px" }}>
                {/* Category Label */}
                <div style={{
                  fontSize: "11px",
                  fontWeight: 700,
                  color: "#0073ea",
                  textTransform: "uppercase",
                  letterSpacing: "0.5px",
                  marginBottom: "6px",
                  paddingLeft: "4px",
                  display: "flex",
                  alignItems: "center",
                  gap: "5px"
                }}>
                  <span>{cat.icon}</span>
                  <span>{cat.category}</span>
                </div>

                {/* Questions */}
                {cat.questions.map((q, qi) => (
                  <button
                    key={qi}
                    onClick={() => handleSampleClick(q)}
                    style={{
                      width: "100%",
                      textAlign: "left",
                      background: "none",
                      border: "1px solid #e9ecef",
                      borderRadius: "8px",
                      padding: "8px 10px",
                      marginBottom: "5px",
                      cursor: "pointer",
                      fontSize: "12px",
                      color: "#333",
                      lineHeight: "1.4",
                      transition: "all 0.15s ease",
                      boxSizing: "border-box"
                    }}
                    onMouseEnter={e => {
                      (e.target as HTMLButtonElement).style.background = "#f0f6ff"
                      ;(e.target as HTMLButtonElement).style.borderColor = "#0073ea"
                      ;(e.target as HTMLButtonElement).style.color = "#0073ea"
                    }}
                    onMouseLeave={e => {
                      (e.target as HTMLButtonElement).style.background = "none"
                      ;(e.target as HTMLButtonElement).style.borderColor = "#e9ecef"
                      ;(e.target as HTMLButtonElement).style.color = "#333"
                    }}
                  >
                    {q}
                  </button>
                ))}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Main Chat Container */}
      <div style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        overflow: "hidden",
        boxSizing: "border-box",
        minWidth: 0
      }}>

        {/* Header */}
        <div style={{
          padding: "16px 24px",
          borderBottom: "1px solid #e9ecef",
          background: "#ffffff",
          flexShrink: 0,
          display: "flex",
          alignItems: "center",
          gap: "12px"
        }}>
          {/* Toggle Sidebar Button */}
          {!sidebarOpen && (
            <button
              onClick={() => setSidebarOpen(true)}
              style={{
                background: "#f0f6ff",
                border: "1px solid #d0e8ff",
                borderRadius: "8px",
                padding: "6px 10px",
                cursor: "pointer",
                fontSize: "16px",
                color: "#0073ea"
              }}>
              ☰
            </button>
          )}
          <div>
            <h2 style={{ margin: 0, fontSize: "17px", fontWeight: 700, color: "#1a1a2e" }}>
              🤖 Monday.com BI Agent
            </h2>
            <p style={{ margin: "2px 0 0", fontSize: "12px", color: "#888" }}>
              Ask founder-level business questions
            </p>
          </div>
        </div>

        {/* Messages Area */}
        <div style={{
          flex: 1,
          overflowY: "auto",
          padding: "20px 24px",
          display: "flex",
          flexDirection: "column",
          gap: "16px",
          boxSizing: "border-box"
        }}>
          {messages.length === 0 && (
            <div style={{
              textAlign: "center",
              color: "#aaa",
              marginTop: "60px",
              fontSize: "14px"
            }}>
              <div style={{ fontSize: "36px", marginBottom: "12px" }}>📊</div>
              <div>Ask a business question to get started</div>
              <div style={{ marginTop: "8px", fontSize: "13px", color: "#bbb" }}>
                Pick a sample question from the left or type your own
              </div>
            </div>
          )}

          {messages.map((m, i) => (
            <div key={i} style={{
              display: "flex",
              flexDirection: "column",
              alignItems: m.role === "user" ? "flex-end" : "flex-start",
              width: "100%"
            }}>
              <div style={{
                fontSize: "11px", color: "#aaa", marginBottom: "4px",
                paddingLeft: m.role === "user" ? "0" : "4px",
                paddingRight: m.role === "user" ? "4px" : "0"
              }}>
                {m.role === "user" ? "You" : "BI Agent"}
              </div>

              <div style={{
                padding: "12px 16px",
                borderRadius: m.role === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
                background: m.role === "user" ? "#0073ea" : "#f0f2f5",
                color: m.role === "user" ? "white" : "#1a1a2e",
                maxWidth: "80%",
                width: "fit-content",
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
                fontSize: "14px",
                lineHeight: "1.6",
                boxSizing: "border-box"
              }}>
                {m.content}
              </div>

              {m.trace && m.trace.length > 0 && (
                <button
                  onClick={() => setShowTrace(showTrace === m.trace ? null : m.trace!)}
                  style={{
                    marginTop: "6px", fontSize: "12px", color: "#0073ea",
                    background: "none", border: "1px solid #d0e8ff",
                    borderRadius: "12px", padding: "3px 10px",
                    cursor: "pointer", alignSelf: "flex-start"
                  }}>
                  🔍 {showTrace === m.trace ? "Hide" : "View"} agent trace ({m.trace.length} calls)
                </button>
              )}

              {m.trace && showTrace === m.trace && (
                <div style={{
                  marginTop: "8px", background: "#fafafa",
                  border: "1px solid #e9ecef", borderRadius: "12px",
                  padding: "12px 16px", width: "100%", boxSizing: "border-box"
                }}>
                  <div style={{ fontSize: "12px", fontWeight: 700, marginBottom: "8px", color: "#555" }}>
                    Agent Trace
                  </div>
                  {showTrace.map((t, j) => (
                    <div key={j} style={{
                      background: "white", border: "1px solid #eee",
                      borderRadius: "8px", padding: "8px 12px",
                      marginBottom: "6px", fontSize: "13px"
                    }}>
                      <span style={{ fontWeight: 600 }}>🔧 {t.tool}</span>
                      <span style={{ color: "#888", marginLeft: "10px" }}>Status: {t.status}</span>
                      {t.records_returned !== undefined && (
                        <span style={{ color: "#0073ea", marginLeft: "10px" }}>
                          {t.records_returned} records
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "#888", fontSize: "13px" }}>
              <div style={{
                width: "8px", height: "8px", borderRadius: "50%",
                background: "#0073ea", animation: "pulse 1s infinite"
              }} />
              Thinking...
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div style={{
          padding: "16px 24px",
          borderTop: "1px solid #e9ecef",
          background: "#ffffff",
          flexShrink: 0,
          boxSizing: "border-box"
        }}>
          <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === "Enter" && !e.shiftKey && sendMessage()}
              placeholder="Ask a business question..."
              style={{
                flex: 1, padding: "12px 16px", borderRadius: "24px",
                border: "1px solid #e0e0e0", fontSize: "14px",
                outline: "none", background: "#f5f6fa",
                color: "#1a1a2e", caretColor: "#0073ea",
                boxSizing: "border-box"
              }}
            />
            <button
              onClick={() => sendMessage()}
              disabled={loading}
              style={{
                padding: "12px 20px",
                background: loading ? "#ccc" : "#0073ea",
                color: "white", border: "none", borderRadius: "24px",
                cursor: loading ? "not-allowed" : "pointer",
                fontSize: "14px", fontWeight: 600, flexShrink: 0
              }}>
              {loading ? "..." : "Send"}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}