import { ArrowLeft, Volume2, VolumeX, Zap, Eye } from 'lucide-react';
import { useState } from 'react';
import { IconButton } from './IconButton';
import { GlassCard } from './GlassCard';

interface SettingsScreenProps {
  onBack: () => void;
  settings: GameSettings;
  onSettingsChange: (settings: GameSettings) => void;
}

export interface GameSettings {
  masterVolume: number;
  musicVolume: number;
  sfxVolume: number;
  difficulty: 'easy' | 'medium' | 'hard' | 'extreme';
  quality: 'low' | 'medium' | 'high' | 'ultra';
  particleEffects: boolean;
  screenShake: boolean;
  showFPS: boolean;
}

export function SettingsScreen({ onBack, settings, onSettingsChange }: SettingsScreenProps) {
  const updateSetting = <K extends keyof GameSettings>(key: K, value: GameSettings[K]) => {
    onSettingsChange({ ...settings, [key]: value });
  };

  const resetToDefaults = () => {
    onSettingsChange({
      masterVolume: 75,
      musicVolume: 65,
      sfxVolume: 80,
      difficulty: 'medium',
      quality: 'high',
      particleEffects: true,
      screenShake: true,
      showFPS: false,
    });
  };

  const difficultyOptions = [
    { id: 'easy' as const, name: 'Easy', description: 'Slower ball, more lives' },
    { id: 'medium' as const, name: 'Medium', description: 'Balanced gameplay' },
    { id: 'hard' as const, name: 'Hard', description: 'Faster ball, fewer lives' },
    { id: 'extreme' as const, name: 'Extreme', description: 'Maximum challenge' },
  ];

  const qualityOptions = [
    { id: 'low' as const, name: 'Low', description: 'Best performance' },
    { id: 'medium' as const, name: 'Medium', description: 'Balanced' },
    { id: 'high' as const, name: 'High', description: 'Enhanced visuals' },
    { id: 'ultra' as const, name: 'Ultra', description: 'Maximum quality' },
  ];

  return (
    <div className="relative w-full min-h-screen p-8">
      {/* Background */}
      <div 
        className="absolute inset-0 -z-10"
        style={{
          background: `
            radial-gradient(circle at 20% 20%, rgba(64, 224, 208, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 140, 0, 0.1) 0%, transparent 50%),
            var(--bg-dark)
          `,
        }}
      />

      <div className="max-w-3xl mx-auto">
        <GlassCard className="p-8">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-4">
              <IconButton size="md" onClick={onBack}>
                <ArrowLeft size={20} />
              </IconButton>
              <h2 className="text-3xl font-bold" style={{ color: 'var(--color-cyan)' }}>
                Settings
              </h2>
            </div>
            <button 
              onClick={resetToDefaults}
              className="glass px-4 py-2 rounded-lg text-sm text-[var(--color-foreground)]/60 hover:text-[var(--color-foreground)] hover:box-glow-purple transition-all duration-300"
            >
              Reset to Defaults
            </button>
          </div>

          {/* Audio Section */}
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-4">
              {settings.masterVolume === 0 ? (
                <VolumeX size={24} className="text-[var(--color-cyan)]" />
              ) : (
                <Volume2 size={24} className="text-[var(--color-cyan)]" />
              )}
              <h3 className="text-xl font-semibold">Audio</h3>
            </div>

            <div className="ml-9 space-y-4">
              <VolumeSlider
                label="Master Volume"
                value={settings.masterVolume}
                onChange={(value) => updateSetting('masterVolume', value)}
              />
              <VolumeSlider
                label="Music Volume"
                value={settings.musicVolume}
                onChange={(value) => updateSetting('musicVolume', value)}
              />
              <VolumeSlider
                label="Sound Effects Volume"
                value={settings.sfxVolume}
                onChange={(value) => updateSetting('sfxVolume', value)}
              />
            </div>
          </div>

          {/* Divider */}
          <div className="h-px bg-[var(--color-border)]/30 mb-8" />

          {/* Difficulty Section */}
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-4">
              <Zap size={24} className="text-[var(--color-orange)]" />
              <h3 className="text-xl font-semibold">Difficulty</h3>
            </div>

            <div className="ml-9 grid grid-cols-2 gap-3">
              {difficultyOptions.map((option) => (
                <button
                  key={option.id}
                  onClick={() => updateSetting('difficulty', option.id)}
                  className={`p-4 rounded-lg border-2 transition-all duration-300 text-left ${
                    settings.difficulty === option.id
                      ? 'border-[var(--color-orange)] bg-[var(--color-orange)]/10 box-glow-orange'
                      : 'border-[var(--color-border)]/30 glass hover:border-[var(--color-border)]/50 hover:-translate-y-0.5'
                  }`}
                >
                  <p className="font-semibold">{option.name}</p>
                  <p className="text-xs text-[var(--color-foreground)]/60 mt-1">
                    {option.description}
                  </p>
                </button>
              ))}
            </div>
          </div>

          {/* Divider */}
          <div className="h-px bg-[var(--color-border)]/30 mb-8" />

          {/* Visual Quality Section */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <Eye size={24} className="text-[var(--color-purple)]" />
              <h3 className="text-xl font-semibold">Visual Quality</h3>
            </div>

            <div className="ml-9">
              <div className="grid grid-cols-2 gap-3 mb-6">
                {qualityOptions.map((option) => (
                  <button
                    key={option.id}
                    onClick={() => updateSetting('quality', option.id)}
                    className={`p-4 rounded-lg border-2 transition-all duration-300 text-left ${
                      settings.quality === option.id
                        ? 'border-[var(--color-purple)] bg-[var(--color-purple)]/10 box-glow-purple'
                        : 'border-[var(--color-border)]/30 glass hover:border-[var(--color-border)]/50 hover:-translate-y-0.5'
                    }`}
                  >
                    <p className="font-semibold">{option.name}</p>
                    <p className="text-xs text-[var(--color-foreground)]/60 mt-1">
                      {option.description}
                    </p>
                  </button>
                ))}
              </div>

              {/* Toggle Switches */}
              <div className="space-y-3">
                <ToggleSwitch
                  label="Particle Effects"
                  description="Enable particle explosions and trails"
                  checked={settings.particleEffects}
                  onChange={(checked) => updateSetting('particleEffects', checked)}
                />
                <ToggleSwitch
                  label="Screen Shake"
                  description="Camera shake on impacts"
                  checked={settings.screenShake}
                  onChange={(checked) => updateSetting('screenShake', checked)}
                />
                <ToggleSwitch
                  label="Show FPS Counter"
                  description="Display frames per second"
                  checked={settings.showFPS}
                  onChange={(checked) => updateSetting('showFPS', checked)}
                />
              </div>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}

function VolumeSlider({ label, value, onChange }: { label: string; value: number; onChange: (value: number) => void }) {
  return (
    <div>
      <div className="flex justify-between mb-2">
        <label className="text-sm font-medium">{label}</label>
        <span className="text-sm text-[var(--color-foreground)]/60">{value}%</span>
      </div>
      <div className="relative">
        <div className="h-1 rounded-full bg-[var(--bg-muted)]/30" />
        <div 
          className="absolute top-0 h-1 rounded-full"
          style={{
            width: `${value}%`,
            background: 'linear-gradient(90deg, var(--color-cyan), var(--color-purple))',
          }}
        />
        <input
          type="range"
          min="0"
          max="100"
          value={value}
          onChange={(e) => onChange(parseInt(e.target.value))}
          className="absolute top-0 w-full h-1 opacity-0 cursor-pointer"
        />
        <div
          className="absolute top-1/2 -translate-y-1/2 w-4 h-4 rounded-full bg-[var(--color-cyan)] border-2 border-white transition-all duration-150 cursor-pointer hover:scale-110"
          style={{
            left: `calc(${value}% - 8px)`,
            boxShadow: '0 0 15px rgba(64, 224, 208, 0.5)',
          }}
        />
      </div>
    </div>
  );
}

function ToggleSwitch({ label, description, checked, onChange }: { label: string; description: string; checked: boolean; onChange: (checked: boolean) => void }) {
  return (
    <div className="glass rounded-lg p-3 flex items-center justify-between">
      <div className="cursor-pointer" onClick={() => onChange(!checked)}>
        <p className="text-sm font-medium">{label}</p>
        <p className="text-xs text-[var(--color-foreground)]/60 mt-1">{description}</p>
      </div>
      <button
        onClick={() => onChange(!checked)}
        className={`relative w-11 h-6 rounded-full transition-all duration-200 ${
          checked ? 'bg-[var(--color-cyan)]' : 'bg-[var(--bg-muted)]/40'
        }`}
        style={checked ? { boxShadow: '0 0 15px rgba(64, 224, 208, 0.5)' } : {}}
      >
        <div
          className={`absolute top-1/2 -translate-y-1/2 w-5 h-5 rounded-full bg-white shadow-md transition-all duration-200 ${
            checked ? 'left-[calc(100%-22px)]' : 'left-0.5'
          }`}
        />
      </button>
    </div>
  );
}
