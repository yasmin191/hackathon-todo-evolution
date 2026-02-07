/**
 * Multi-language translations for Todo Evolution
 * Supports English (en) and Urdu (ur)
 */

export type Language = "en" | "ur";

export interface Translations {
  // Common
  appName: string;
  loading: string;
  error: string;
  success: string;
  cancel: string;
  save: string;
  delete: string;
  edit: string;
  close: string;
  confirm: string;
  yes: string;
  no: string;

  // Navigation
  home: string;
  tasks: string;
  chat: string;
  settings: string;
  login: string;
  logout: string;
  register: string;

  // Tasks
  addTask: string;
  editTask: string;
  deleteTask: string;
  taskTitle: string;
  taskDescription: string;
  taskPriority: string;
  taskDueDate: string;
  taskTags: string;
  taskCompleted: string;
  taskPending: string;
  noTasks: string;
  markComplete: string;
  markIncomplete: string;

  // Priority levels
  priorityLow: string;
  priorityMedium: string;
  priorityHigh: string;
  priorityUrgent: string;

  // Chat
  chatPlaceholder: string;
  sendMessage: string;
  chatWelcome: string;
  chatHelp: string;

  // Filters
  filterAll: string;
  filterActive: string;
  filterCompleted: string;
  filterByPriority: string;
  filterByTag: string;
  searchTasks: string;

  // Auth
  email: string;
  password: string;
  confirmPassword: string;
  forgotPassword: string;
  loginButton: string;
  registerButton: string;
  noAccount: string;
  hasAccount: string;

  // Voice
  voiceStart: string;
  voiceStop: string;
  voiceListening: string;
  voiceProcessing: string;

  // Errors
  errorNetwork: string;
  errorAuth: string;
  errorNotFound: string;
  errorServer: string;

  // Success messages
  taskCreated: string;
  taskUpdated: string;
  taskDeleted: string;
  taskCompleteSuccess: string;
}

export const translations: Record<Language, Translations> = {
  en: {
    // Common
    appName: "Todo Evolution",
    loading: "Loading...",
    error: "Error",
    success: "Success",
    cancel: "Cancel",
    save: "Save",
    delete: "Delete",
    edit: "Edit",
    close: "Close",
    confirm: "Confirm",
    yes: "Yes",
    no: "No",

    // Navigation
    home: "Home",
    tasks: "Tasks",
    chat: "Chat",
    settings: "Settings",
    login: "Login",
    logout: "Logout",
    register: "Register",

    // Tasks
    addTask: "Add Task",
    editTask: "Edit Task",
    deleteTask: "Delete Task",
    taskTitle: "Title",
    taskDescription: "Description",
    taskPriority: "Priority",
    taskDueDate: "Due Date",
    taskTags: "Tags",
    taskCompleted: "Completed",
    taskPending: "Pending",
    noTasks: "No tasks yet. Add your first task!",
    markComplete: "Mark as Complete",
    markIncomplete: "Mark as Incomplete",

    // Priority levels
    priorityLow: "Low",
    priorityMedium: "Medium",
    priorityHigh: "High",
    priorityUrgent: "Urgent",

    // Chat
    chatPlaceholder: "Type a message or command...",
    sendMessage: "Send",
    chatWelcome: "Hello! I'm your AI assistant. How can I help you manage your tasks today?",
    chatHelp: "You can ask me to add tasks, list your tasks, mark them complete, or search for specific tasks.",

    // Filters
    filterAll: "All",
    filterActive: "Active",
    filterCompleted: "Completed",
    filterByPriority: "By Priority",
    filterByTag: "By Tag",
    searchTasks: "Search tasks...",

    // Auth
    email: "Email",
    password: "Password",
    confirmPassword: "Confirm Password",
    forgotPassword: "Forgot Password?",
    loginButton: "Sign In",
    registerButton: "Sign Up",
    noAccount: "Don't have an account?",
    hasAccount: "Already have an account?",

    // Voice
    voiceStart: "Start Voice Input",
    voiceStop: "Stop",
    voiceListening: "Listening...",
    voiceProcessing: "Processing...",

    // Errors
    errorNetwork: "Network error. Please check your connection.",
    errorAuth: "Authentication failed. Please login again.",
    errorNotFound: "Resource not found.",
    errorServer: "Server error. Please try again later.",

    // Success messages
    taskCreated: "Task created successfully!",
    taskUpdated: "Task updated successfully!",
    taskDeleted: "Task deleted successfully!",
    taskCompleteSuccess: "Task marked as complete!",
  },

  ur: {
    // Common - اردو
    appName: "ٹوڈو ایوولیوشن",
    loading: "لوڈ ہو رہا ہے...",
    error: "غلطی",
    success: "کامیابی",
    cancel: "منسوخ",
    save: "محفوظ کریں",
    delete: "حذف کریں",
    edit: "ترمیم",
    close: "بند کریں",
    confirm: "تصدیق",
    yes: "ہاں",
    no: "نہیں",

    // Navigation
    home: "ہوم",
    tasks: "کام",
    chat: "چیٹ",
    settings: "ترتیبات",
    login: "لاگ ان",
    logout: "لاگ آؤٹ",
    register: "رجسٹر",

    // Tasks
    addTask: "کام شامل کریں",
    editTask: "کام میں ترمیم",
    deleteTask: "کام حذف کریں",
    taskTitle: "عنوان",
    taskDescription: "تفصیل",
    taskPriority: "ترجیح",
    taskDueDate: "آخری تاریخ",
    taskTags: "ٹیگز",
    taskCompleted: "مکمل",
    taskPending: "زیر التواء",
    noTasks: "ابھی کوئی کام نہیں۔ اپنا پہلا کام شامل کریں!",
    markComplete: "مکمل نشان لگائیں",
    markIncomplete: "نامکمل نشان لگائیں",

    // Priority levels
    priorityLow: "کم",
    priorityMedium: "درمیانہ",
    priorityHigh: "اہم",
    priorityUrgent: "فوری",

    // Chat
    chatPlaceholder: "پیغام یا کمانڈ لکھیں...",
    sendMessage: "بھیجیں",
    chatWelcome: "السلام علیکم! میں آپ کا AI معاون ہوں۔ آج میں آپ کے کاموں کا انتظام کرنے میں کیسے مدد کر سکتا ہوں؟",
    chatHelp: "آپ مجھ سے کام شامل کرنے، اپنے کاموں کی فہرست دیکھنے، انہیں مکمل نشان لگانے، یا مخصوص کاموں کی تلاش کرنے کے لیے کہہ سکتے ہیں۔",

    // Filters
    filterAll: "تمام",
    filterActive: "فعال",
    filterCompleted: "مکمل",
    filterByPriority: "ترجیح کے لحاظ سے",
    filterByTag: "ٹیگ کے لحاظ سے",
    searchTasks: "کام تلاش کریں...",

    // Auth
    email: "ای میل",
    password: "پاس ورڈ",
    confirmPassword: "پاس ورڈ کی تصدیق",
    forgotPassword: "پاس ورڈ بھول گئے؟",
    loginButton: "سائن ان",
    registerButton: "سائن اپ",
    noAccount: "اکاؤنٹ نہیں ہے؟",
    hasAccount: "پہلے سے اکاؤنٹ ہے؟",

    // Voice
    voiceStart: "آواز سے لکھیں",
    voiceStop: "رکیں",
    voiceListening: "سن رہا ہوں...",
    voiceProcessing: "پروسیسنگ...",

    // Errors
    errorNetwork: "نیٹ ورک کی غلطی۔ براہ کرم اپنا کنکشن چیک کریں۔",
    errorAuth: "توثیق ناکام۔ براہ کرم دوبارہ لاگ ان کریں۔",
    errorNotFound: "مواد نہیں ملا۔",
    errorServer: "سرور کی غلطی۔ براہ کرم بعد میں دوبارہ کوشش کریں۔",

    // Success messages
    taskCreated: "کام کامیابی سے بنایا گیا!",
    taskUpdated: "کام کامیابی سے اپ ڈیٹ ہوا!",
    taskDeleted: "کام کامیابی سے حذف ہوا!",
    taskCompleteSuccess: "کام مکمل نشان لگا دیا گیا!",
  },
};

/**
 * Get translation for a key
 */
export function t(key: keyof Translations, lang: Language = "en"): string {
  return translations[lang][key] || translations.en[key] || key;
}

/**
 * Get all translations for a language
 */
export function getTranslations(lang: Language): Translations {
  return translations[lang];
}

/**
 * Check if language is RTL (Right-to-Left)
 */
export function isRTL(lang: Language): boolean {
  return lang === "ur";
}

/**
 * Get language direction
 */
export function getDirection(lang: Language): "ltr" | "rtl" {
  return isRTL(lang) ? "rtl" : "ltr";
}
