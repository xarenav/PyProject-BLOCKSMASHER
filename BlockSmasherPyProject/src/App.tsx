import { useState } from 'react';
import { MainMenu } from './components/MainMenu';
import { MapsScreen } from './components/MapsScreen';
import { LeaderboardScreen } from './components/LeaderboardScreen';
import { SettingsScreen, GameSettings } from './components/SettingsScreen';
import { GameScreen } from './components/GameScreen';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<'menu' | 'maps' | 'leaderboard' | 'settings' | 'game'>('menu');
  const [selectedMapId, setSelectedMapId] = useState<number>(1);
  const [unlockedLevels, setUnlockedLevels] = useState<number[]>([1]); // Start with level 1 unlocked
  const [settings, setSettings] = useState<GameSettings>({
    masterVolume: 75,
    musicVolume: 65,
    sfxVolume: 80,
    difficulty: 'medium',
    quality: 'high',
    particleEffects: true,
    screenShake: true,
    showFPS: false,
  });

  const handleSelectMap = (mapId: number) => {
    setSelectedMapId(mapId);
    setCurrentScreen('game');
  };

  const handleLevelComplete = (levelId: number) => {
    // Unlock the next level
    const nextLevel = levelId + 1;
    if (!unlockedLevels.includes(nextLevel)) {
      setUnlockedLevels([...unlockedLevels, nextLevel]);
    }
  };

  return (
    <div className="size-full min-h-screen">
      {currentScreen === 'menu' && (
        <MainMenu onNavigate={(screen) => setCurrentScreen(screen as any)} />
      )}
      {currentScreen === 'maps' && (
        <MapsScreen 
          onBack={() => setCurrentScreen('menu')} 
          onSelectMap={handleSelectMap}
          unlockedLevels={unlockedLevels}
        />
      )}
      {currentScreen === 'leaderboard' && (
        <LeaderboardScreen onBack={() => setCurrentScreen('menu')} />
      )}
      {currentScreen === 'settings' && (
        <SettingsScreen 
          onBack={() => setCurrentScreen('menu')} 
          settings={settings}
          onSettingsChange={setSettings}
        />
      )}
      {currentScreen === 'game' && (
        <GameScreen 
          onBack={() => setCurrentScreen('maps')} 
          levelId={selectedMapId}
          settings={settings}
          onLevelComplete={handleLevelComplete}
        />
      )}
    </div>
  );
}
