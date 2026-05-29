import ChatPage
  from "./pages/ChatPage";

import OnboardingPage
  from "./pages/OnboardingPage";

import {
  useChatStore
} from "./store/chatStore";

export default function App() {

  const {
    initialized
  } = useChatStore();

  return initialized

    ? <ChatPage />

    : <OnboardingPage />;
}