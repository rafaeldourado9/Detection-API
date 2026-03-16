import { useCallback, useSyncExternalStore } from "react";

function getToken() {
  return localStorage.getItem("token");
}

const listeners = new Set<() => void>();

function subscribe(cb: () => void) {
  listeners.add(cb);
  return () => listeners.delete(cb);
}

function notify() {
  listeners.forEach((cb) => cb());
}

export function useAuth() {
  const token = useSyncExternalStore(subscribe, getToken);

  const setToken = useCallback((t: string) => {
    localStorage.setItem("token", t);
    notify();
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("token");
    notify();
  }, []);

  return { token, setToken, logout };
}
