export const PROVIDER_ICONS = {
  gpt4: {
    "16": "icons/chatgpt/icon16.png",
    "32": "icons/chatgpt/icon32.png",
    "48": "icons/chatgpt/icon48.png",
    "128": "icons/chatgpt/icon128.png"
  },
  claude: {
    "16": "icons/claude/icon16.png",
    "32": "icons/claude/icon32.png",
    "48": "icons/claude/icon48.png",
    "128": "icons/claude/icon128.png"
  },
  deepseek: {
    "16": "icons/deepseek/icon16.png",
    "32": "icons/deepseek/icon32.png",
    "48": "icons/deepseek/icon48.png",
    "128": "icons/deepseek/icon128.png"
  },
  gemini: {
    "16": "icons/gemini/icon16.png",
    "32": "icons/gemini/icon32.png",
    "48": "icons/gemini/icon48.png",
    "128": "icons/gemini/icon128.png"
  },
  grok: {
    "16": "icons/grok/icon16.png",
    "32": "icons/grok/icon32.png",
    "48": "icons/grok/icon48.png",
    "128": "icons/grok/icon128.png"
  },
  perplexity: {
  "16": "icons/perplexity/icon16.png",
  "32": "icons/perplexity/icon32.png",
  "48": "icons/perplexity/icon48.png",
  "128": "icons/perplexity/icon128.png"
}
};

export const LANGUAGES = {
  en: {
    // Header
    contactDeveloper: "Contact Developer",
    plannerButton: "GoodNotes Planner",
    timeAppButton: "Pomodoro Timer",
    
    // Hero Section
    heroTitle: "Pick Your AI Model",
    heroSubtitle: "Customize your experience with smart AI assistance",
    
    // Appearance Section
    appearance: "App Settings",
    theme: "Theme",
    themeSystem: "System Default",
    themeLight: "Light Mode",
    themeDark: "Dark Mode",
    
    // AI Model Selection
    aiModelSelection: "Choose AI Model",

    extensionSettings: "Extension Settings",
    commentSetting: "YouTube Comments",
    commentSettingDesc: "Include comments when processing YouTube videos (may increase processing time)",
    
    // Prompt Template
    promptTabs: "Prompt Templates", // en
    defaultTemplateName: "Prompt", // en
    defaultPrompt: `[Request]
Please read the following content and:

1. Core Message: Distill the central thesis into one impactful sentence that captures the essence.

2. Key Points: Craft a 5-sentence synopsis covering critical arguments, flow, and implications.

3. Analytical Framework:
   • Argument Structure: Map the logical progression, identify premises/conclusions
   • Evidence Assessment: Evaluate data quality, methodology, source credibility
   • Critical Evaluation: Pinpoint fallacies, bias, rhetorical tactics, and unstated assumptions

4. Contextual Dimensions:
   • Creator Perspective: Infer intent, ideological position, and potential conflicts of interest
   • Socio-Historical Context: Place content within relevant events, movements, and discourse
   • Intellectual Lineage: Connect to established literature, competing theories, and ongoing debates

5. Audience Analysis:
   • Target Demographics: Identify intended readers/viewers by age, expertise, interests, viewpoints
   • Reception Patterns: Predict varied responses across different demographic segments
   • Engagement Metrics: Note social sharing, comments, citations as indicators of impact

6. SWOT Assessment:
   • Strengths: Three most compelling, original, or well-executed elements
   • Weaknesses: Three areas of logical vulnerability, insufficient evidence, or missed opportunities
   • Opportunities: Potential extensions, applications, or developmental directions
   • Threats: Countervailing views, limitations, or implementation challenges

7. Intellectual Expansion:
   • Related Domains: Suggest three fields offering valuable cross-pollination
   • Practical Applications: Outline actionable implementations for individuals/organizations
   • Further Inquiry: Formulate three high-yield questions for deeper investigation

8. Customization of Response Style (Language and Tone)
Optimize the response to be clear, insightful, and well-structured using precise wording and terminology.
Consider the user's preference for formal, concise, or narrative-style explanations when crafting the response.`,
    deleteTemplateTitle: "Delete Template", // en
    deleteTemplateConfirm: "Are you sure you want to delete this template?", // en
    deleteActiveTemplateError: "Cannot delete the active template. Please select another template first.", // en
    deleteLastTemplateError: "Cannot delete the last template.", // en
    
    // Pro Tips Section
    youtube: "YouTube",
    threads: "Threads",
    instagram: "Instagram",
    proTips: "Pro Tips",
    shortcutTipTitle: "Work faster with shortcuts",
    shortcutTipDesc: "Set up custom shortcuts in your browser’s extension settings.",
    edgeShortcuts: "Set up Edge shortcuts →",
    chromeShortcuts: "Set up Chrome shortcuts →",
    iconTipTitle: "Easily spot your AI model",
    iconTipDesc: "The extension icon changes based on the AI model you're using.",
    
    // Social Section
    followUs: "Follow Us",
    socialDesc: "Discover more content on productivity and self-improvement!",
    
    // Buttons
    saveChanges: "Save Changes",
    resetSettings: "Reset Settings",
    resetStorage: "Reset Storage",
    
    // Footer
    copyright: "© 2025 ChatPage Extension. All rights reserved.",
    privacyPolicy: "Privacy Policy",
    termsOfUse: "Terms of Use",
    contactSupport: "Get Support",

    // AI Provider Names & Descriptions
    gpt4Name: "ChatGPT",
    gpt4Description: "A powerful AI for writing, problem-solving, and more",
    claudeName: "Claude",
    claudeDescription: "Great for in-depth analysis and detailed explanations",
    deepseekName: "DeepSeek",
    deepseekDescription: "Specialized in coding and technical insights",
    geminiName: "Gemini",
    geminiDescription: "Google’s AI with strong analytical skills",
    grokName: "Grok",
    grokDescription: "Real-time data analysis with unique insights",
    perplexityName: "Perplexity",
    perplexityDescription: "Advanced AI with real-time knowledge and citations",

    // Pro Tips
    shortcutEdge: "Set up Edge shortcuts",
    shortcutChrome: "Set up Chrome shortcuts",
    copyText: "Copy",
    copiedText: "Copied!",
    
    // Social
    socialTitle: "More Channels",
    youtubeTitle: "Learn on YouTube",
    youtubeDesc: "Watch step-by-step guides and pro tips.",
    threadsTitle: "Ask on Threads",
    threadsDesc: "Have questions? Ask and learn from the community.",
    instaTitle: "Quick Updates on Instagram",
    instaDesc: "Get the latest features and tips in real time.",

    // Reset Storage
    resetStorageConfirm: "Are you sure you want to reset all storage? This action cannot be undone.",
    resetStorageComplete: "All settings and templates have been reset.",
    resetTemplatesConfirm: "Are you sure you want to reset all settings?",
    settingsSaved: "Settings have been saved.",

    // Storage Space
    templateOptimized: "Template storage locations optimized ({0} changed)",
    storageSpaceLimit: "Settings size has reached the limit. Delete some templates to enable synchronization.",
    templateSaveError: "Error saving template: {0}",
    templateDeleteError: "Error deleting template: {0}",
    initializationError: "Error during initialization: {0}",
    templateMovedSync: "Template {0} moved to cloud storage",
    templateMovedLocal: "Template {0} moved to local storage"
  },
  ko: {
    // Header
    contactDeveloper: "궁금해요",
    plannerButton: "굿노트 플래너",
    timeAppButton: "뽀모도로 타이머앱",
    
    // Hero Section
    heroTitle: "AI 모델 선택하기",
    heroSubtitle: "필요한 AI를 골라 더 스마트하게 사용하세요",
    
    // Appearance Section
    appearance: "앱 설정",
    theme: "테마",
    themeSystem: "시스템 기본값",
    themeLight: "라이트 모드",
    themeDark: "다크 모드",
    
    // AI Model Selection
    aiModelSelection: "AI 모델 선택",

    extensionSettings: "확장 앱 설정",
    commentSetting: "유튜브 댓글",
    commentSettingDesc: "유튜브 영상 처리 시 댓글 포함 (처리 시간이 늘어날 수 있음)",
    
    // Prompt Template
    promptTabs: "프롬프트 템플릿", // ko
    defaultTemplateName: "프롬프트", // ko
    defaultPrompt: `[요청]
다음 콘텐츠를 읽고 다음 항목에 대해 답변해주세요:

1. 가장 중요한 결론 요약  
핵심 메시지를 한 문장으로 요약해주세요. 사용자에게 메시지를 빠르게 전달할 수 있는 명확하고 간결한 설명을 제공해주세요.

2. 주요 내용 요약  
주요 내용을 세 줄로 요약해주세요. 주요 흐름과 중요한 주제를 놓치지 않고 다루도록 하되, 간단하고 명확하게 정리해주세요.

3. 핵심 포인트에 대한 응답  
유튜브: 댓글에서 제기된 질문이나 요점에 기반하여 간결하게 응답해주세요.  
기사: 콘텐츠에서 제시된 주요 주장과 논점에 대해 간결하게 다루어주세요.

4. 추가 정보  
콘텐츠와 관련하여 더 깊은 관심을 가질 수 있는 사용자를 위해 간단한 추가 설명을 제공해주세요. 필요한 경우, 추가 자료나 참고 문헌을 제안해주세요.

5. 언어 선호도  
모든 내용을 사용자의 시스템 언어로 제공해주세요. 사용자의 시스템 언어가 한국어로 설정되어 있다면 한국어로, 일본어로 설정되어 있다면 일본어로 응답해주세요. 설명과 대화가 사용자의 시스템 언어와 일치하도록 해주세요.`,
    
    // 빈 템플릿 가이드 수정
    emptyTemplateGuide: `[콘텐츠 분석 요청]
다음 콘텐츠를 읽고 다음의 구조에 맞춰 분석해 주세요.

1. 핵심 명제: 본질을 포착하는 한 문장으로 중심 주장 압축.

2. 주요 요점: 핵심 논점, 흐름, 함의를 포괄하는 5문장 요약.

3. 분석 구조:
   • 논증 구조: 논리 전개, 전제-결론 관계 정밀 매핑
   • 증거 평가: 데이터 품질, 방법론, 출처 신뢰성 검증
   • 비판적 검토: 논리적 오류, 편향성, 수사적 전략, 암묵적 가정 식별

4. 맥락적 차원:
   • 제작자 관점: 의도, 이념적 위치, 잠재적 이해충돌 추론
   • 사회역사적 배경: 관련 사건, 운동, 담론 속 위치 파악
   • 지적 계보: 기존 문헌, 경쟁 이론, 현재 논쟁과의 연결성

5. 수용자 분석:
   • 목표 독자층: 연령, 전문성, 관심사, 관점별 대상 독자 식별
   • 반응 패턴: 다양한 인구 집단별 예상 반응 예측
   • 참여 지표: 공유, 댓글, 인용 등 영향력 지표 주목

6. SWOT 평가:
   • 강점: 가장 설득력 있는/독창적인/잘 실행된 3가지 요소
   • 약점: 논리적 취약점, 불충분한 증거, 놓친 기회 3가지
   • 기회: 잠재적 확장, 응용, 발전 방향
   • 위협: 반대 견해, 한계, 실행 과정의 장애물

7. 지적 확장:
   • 관련 분야: 가치 있는 교차 지식을 제공할 3개 영역 제안
   • 실용적 적용: 개인/조직을 위한 실행 가능한 이행 방안
   • 심화 탐구: 더 깊은 조사를 위한 3가지 고수익 질문 제시

8. 맞춤형 응답 스타일 조정 (언어 및 표현 방식)
한국어에 최적화되고 입체적으로 이해 가능하며, 여러 인사이트를 얻을 수 있는 단어와 어휘를 사용하여 응답하세요.
응답 후 사용자가 격식을 선호하는지, 간결한 설명을 원하는지, 서술형 답변을 원하는지 고려하여 표현 방식을 조정하세요.`,
    deleteTemplateTitle: "템플릿 삭제", // ko
    deleteTemplateConfirm: "이 템플릿을 삭제하시겠습니까?", // ko
    deleteActiveTemplateError: "활성화된 템플릿은 삭제할 수 없습니다. 먼저 다른 템플릿을 선택해주세요.", // ko
    deleteLastTemplateError: "마지막 템플릿은 삭제할 수 없습니다.", // ko
    
    // Pro Tips Section
    youtube: "유튜브",
    threads: "쓰레드",
    instagram: "인스타그램",
    proTips: "프로 팁",
    shortcutTipTitle: "단축키로 더 빠르게",
    shortcutTipDesc: "브라우저 확장 프로그램 설정에서 단축키를 설정하세요.",
    edgeShortcuts: "Edge에서 단축키 설정하기",
    chromeShortcuts: "Chrome에서 단축키 설정하기",
    iconTipTitle: "지금 쓰는 AI를 한눈에",
    iconTipDesc: "확장 프로그램 아이콘만 봐도 어떤 AI를 쓰고 있는지 알 수 있어요.",
    
    // Social Section
    followUs: "팔로우하기",
    socialDesc: "생산성과 자기 계발을 위한 더 많은 콘텐츠를 만나보세요!",
    
    // Buttons
    saveChanges: "저장하기",
    resetSettings: "설정 초기화",
    resetStorage: "스토리지 초기화",
    
    // Footer
    copyright: "© 2025 ChatPage Extension. All rights reserved.",
    privacyPolicy: "개인정보 처리방침",
    termsOfUse: "이용약관",
    contactSupport: "고객 지원",

    // AI Provider Names & Descriptions
    gpt4Name: "ChatGPT",
    gpt4Description: "글쓰기부터 문제 해결까지 가능한 강력한 AI",
    claudeName: "Claude",
    claudeDescription: "분석과 설명에 강한 AI",
    deepseekName: "DeepSeek",
    deepseekDescription: "코딩과 기술적 이해에 특화된 AI",
    geminiName: "Gemini",
    geminiDescription: "구글의 강력한 분석형 AI",
    grokName: "Grok",
    grokDescription: "실시간 데이터 분석과 통찰을 제공하는 AI",
    perplexityName: "Perplexity",
    perplexityDescription: "실시간 지식과 인용을 제공하는 AI",

    // Pro Tips
    shortcutEdge: "Edge에서 단축키 설정하기",
    shortcutChrome: "Chrome에서 단축키 설정하기",
    copyText: "복사하기",
    copiedText: "복사 완료!",
    
    // Social
    socialTitle: "다양한 채널에서 만나보세요",
    youtubeTitle: "유튜브에서 배우기",
    youtubeDesc: "작업 과정과 꿀팁을 영상으로 확인하세요.",
    threadsTitle: "쓰레드에서 질문하기",
    threadsDesc: "궁금한 게 있다면 편하게 물어보세요.",
    instaTitle: "인스타그램으로 빠르게",
    instaDesc: "새로운 기능과 꿀팁을 실시간으로 확인하세요.",

    // Reset Storage    
    resetStorageConfirm: "모든 설정과 템플릿을 초기화하시겠습니까? 이 작업은 되돌릴 수 없습니다.",
    resetStorageComplete: "모든 설정과 템플릿이 초기화되었습니다.",
    resetTemplatesConfirm: "모든 설정을 초기화하시겠습니까?",
    settingsSaved: "설정이 저장되었습니다.",

    // Storage Space
    templateOptimized: "템플릿 저장 위치가 최적화되었습니다 ({0}개 변경)",
    storageSpaceLimit: "설정 크기가 제한에 도달했습니다. 일부 템플릿을 삭제하면 동기화가 가능합니다.",
    templateSaveError: "템플릿 저장 중 오류가 발생했습니다: {0}",
    templateDeleteError: "템플릿 삭제 중 오류가 발생했습니다: {0}",
    initializationError: "초기화 중 오류: {0}",
    templateMovedSync: "템플릿 {0}이(가) 클라우드 스토리지로 이동되었습니다",
    templateMovedLocal: "템플릿 {0}이(가) 로컬 스토리지로 이동되었습니다"

  }
};

// 사용자 언어 감지 함수 추가
function detectUserLanguage() {
  try {
    const userLang = navigator.language.toLowerCase().split('-')[0];
    return userLang === 'ko' ? 'ko' : 'en';
  } catch (e) {
    return 'en'; // 기본값은 영어
  }
}

// 언어에 따른 기본 프롬프트 결정
const userLang = detectUserLanguage();
const defaultPromptContent = userLang === 'ko' ? LANGUAGES.ko.defaultPrompt : LANGUAGES.en.defaultPrompt;


export const defaultSettings = {
  theme: 'system',
  fetchComments: false,
  aiProviders: [
    {
      id: 'gpt4',
      name: 'ChatGPT',
      label: 'ChatGPT',
      description: 'Most capable GPT-4 model, great for a wide range of tasks',
      defaultUrl: 'https://chatgpt.com/?model=gpt-4o',
      url: 'https://chatgpt.com/?model=gpt-4o',
      enabled: true,
      selected: true,
      models: [
        {
          id: 'gpt-4o',
          name: 'GPT-4o',
          url: 'https://chatgpt.com/?model=gpt-4o'
        },
        {
          id: 'gpt-4o-jawbone',
          name: 'GPT-4o Schedule Assistant',
          url: 'https://chatgpt.com/?model=gpt-4o-jawbone'
        },
        {
          id: 'gpt-4-5',
          name: 'GPT-4.5',
          url: 'https://chatgpt.com/?model=gpt-4-5'
        },
        {
          id: 'o1',
          name: 'GPT-o1',
          url: 'https://chatgpt.com/?model=o1'
        },
        {
          id: 'o3-mini',
          name: 'GPT-o3-mini',
          url: 'https://chatgpt.com/?model=o3-mini'
        },
        {
          id: 'o3-mini-high',
          name: 'GPT-o3-mini-high',
          url: 'https://chatgpt.com/?model=o3-mini-high'
        },
        {
          id: 'gpt-4o-mini',
          name: 'GPT-4o mini',
          url: 'https://chatgpt.com/?model=gpt-4o-mini'
        },
        {
          id: 'gpt-4',
          name: 'GPT-4',
          url: 'https://chatgpt.com/?model=gpt-4'
        }
      ]
    },
    {
      id: 'deepseek',
      name: 'Deep Seek',
      label: 'Deep Seek',
      description: 'Advanced AI model with deep learning capabilities',
      defaultUrl: 'https://chat.deepseek.com/',
      url: 'https://chat.deepseek.com/',
      enabled: true,
      selected: false
    },
    {
      id: 'claude',
      name: 'Claude',
      label: 'Claude',
      description: "Anthropic's latest AI model with advanced capabilities",
      defaultUrl: 'https://claude.ai/new',
      url: 'https://claude.ai/new',
      enabled: true,
      selected: false
    },
    {
      id: 'gemini',
      name: 'Gemini',
      label: 'Gemini',
      description: "Google's advanced AI model with multimodal capabilities",
      defaultUrl: 'https://gemini.google.com/app',
      url: 'https://gemini.google.com/app',
      enabled: true,
      selected: false
    },
    {
      id: 'grok',
      name: 'Grok',
      label: 'Grok',
      description: "xAI's AI model with a unique perspective on humanity",
      defaultUrl: 'https://x.com/i/grok?focus=1',
      url: 'https://x.com/i/grok?focus=1',
      enabled: true,
      selected: false
    },
    {
      id: 'perplexity',
      name: 'Perplexity',
      label: 'Perplexity',
      description: "Advanced AI with real-time knowledge and citations",
      defaultUrl: 'https://www.perplexity.ai/',
      url: 'https://www.perplexity.ai/',
      enabled: true,
      selected: false
    }
  ],
  customPrompt: defaultPromptContent
};
