import { useCallback, useRef, useState } from "react";
import LeftPanel from "./components/LeftPanel";
import Chat from "./pages/Chat";

const MIN_PCT = 50;
const HIDE_THRESHOLD = 95; // drag past here to hide chat

export default function App() {
  const [splitPct, setSplitPct] = useState(67);
  const [chatHidden, setChatHidden] = useState(false);
  const dragging = useRef(false);

  const onMouseDown = useCallback(() => {
    dragging.current = true;

    function onMouseMove(e: MouseEvent) {
      if (!dragging.current) return;
      const pct = (e.clientX / window.innerWidth) * 100;

      if (pct >= HIDE_THRESHOLD) {
        setChatHidden(true);
        setSplitPct(100);
      } else {
        setChatHidden(false);
        setSplitPct(Math.max(MIN_PCT, pct));
      }
    }

    function onMouseUp() {
      dragging.current = false;
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
    }

    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);
  }, []);

  function showChat() {
    setChatHidden(false);
    setSplitPct(67);
  }

  return (
    <div style={{ display: "flex", height: "100vh", overflow: "hidden" }}>

      <div style={{ width: chatHidden ? "100%" : `${splitPct}%`, overflow: "hidden" }}>
        <LeftPanel />
      </div>

      {/* Drag handle — always mounted so chat stays alive */}
      {!chatHidden && (
        <div
          onMouseDown={onMouseDown}
          style={{
            width: 16,
            cursor: "col-resize",
            flexShrink: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            background: "#f4f4f5",
            borderLeft: "1px solid #e4e4e7",
            borderRight: "1px solid #e4e4e7",
          }}
          onMouseEnter={e => {
            e.currentTarget.style.background = "#e4e4e7";
            (e.currentTarget.querySelector(".dots") as HTMLElement).style.opacity = "1";
          }}
          onMouseLeave={e => {
            e.currentTarget.style.background = "#f4f4f5";
            (e.currentTarget.querySelector(".dots") as HTMLElement).style.opacity = "0.4";
          }}
        >
          <div
            className="dots"
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 3,
              opacity: 0.4,
              transition: "opacity 0.15s",
              pointerEvents: "none",
            }}
          >
            {[...Array(6)].map((_, i) => (
              <div key={i} style={{ width: 3, height: 3, borderRadius: "50%", background: "#71717a" }} />
            ))}
          </div>
        </div>
      )}

      {/* Chat — always mounted, just hidden visually */}
      <div style={{
        width: chatHidden ? 0 : undefined,
        flex: chatHidden ? undefined : 1,
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        visibility: chatHidden ? "hidden" : "visible",
      }}>
        <Chat />
      </div>

      {/* Pull tab — shown when chat is hidden */}
      {chatHidden && (
        <div
          onClick={showChat}
          style={{
            position: "fixed",
            right: 0,
            top: "50%",
            transform: "translateY(-50%)",
            background: "#18181b",
            color: "#fff",
            padding: "12px 6px",
            borderRadius: "6px 0 0 6px",
            cursor: "pointer",
            fontSize: 12,
            writingMode: "vertical-rl",
            letterSpacing: 1,
            userSelect: "none",
          }}
        >
          Chat
        </div>
      )}

    </div>
  );
}
