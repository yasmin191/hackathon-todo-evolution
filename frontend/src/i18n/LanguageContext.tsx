"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { Language, Translations, translations, getDirection } from "./translations";

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: Translations;
  direction: "ltr" | "rtl";
  isRTL: boolean;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

interface LanguageProviderProps {
  children: ReactNode;
  defaultLanguage?: Language;
}

export function LanguageProvider({ children, defaultLanguage = "en" }: LanguageProviderProps) {
  const [language, setLanguageState] = useState<Language>(defaultLanguage);

  // Load saved language from localStorage
  useEffect(() => {
    const savedLang = localStorage.getItem("language") as Language;
    if (savedLang && (savedLang === "en" || savedLang === "ur")) {
      setLanguageState(savedLang);
    }
  }, []);

  // Update document direction when language changes
  useEffect(() => {
    const dir = getDirection(language);
    document.documentElement.dir = dir;
    document.documentElement.lang = language;

    // Add RTL class for styling
    if (dir === "rtl") {
      document.documentElement.classList.add("rtl");
    } else {
      document.documentElement.classList.remove("rtl");
    }
  }, [language]);

  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
    localStorage.setItem("language", lang);
  };

  const value: LanguageContextType = {
    language,
    setLanguage,
    t: translations[language],
    direction: getDirection(language),
    isRTL: language === "ur",
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage(): LanguageContextType {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error("useLanguage must be used within a LanguageProvider");
  }
  return context;
}

// Export a hook for getting just translations
export function useTranslations(): Translations {
  const { t } = useLanguage();
  return t;
}
