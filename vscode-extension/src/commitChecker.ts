import * as vscode from 'vscode';
import { exec } from 'child_process';
import { promisify } from 'util';

const execPromise = promisify(exec);

export class CommitCheckerIntegration {
    private cliPath: string;

    constructor() {
        const config = vscode.workspace.getConfiguration('commit-checker');
        this.cliPath = config.get('cliPath', 'commit-checker');
    }

    /**
     * Execute commit-checker CLI command and return parsed output
     */
    async executeCommand(args: string[]): Promise<string> {
        try {
            const command = `${this.cliPath} ${args.join(' ')}`;
            const { stdout, stderr } = await execPromise(command);

            if (stderr) {
                console.warn(`commit-checker stderr: ${stderr}`);
            }

            return stdout;
        } catch (error) {
            console.error(`commit-checker error: ${error}`);
            throw new Error(`Failed to execute commit-checker: ${error}`);
        }
    }

    /**
     * Get current XP and level
     */
    async getXPStatus(): Promise<{ level: number; xp: number; nextLevel: number } | null> {
        try {
            const output = await this.executeCommand(['--xp']);
            // Parse XP output
            // Example: "⚡ Level 7: Framework Knight\n💫 Total XP: 4,499"

            const levelMatch = output.match(/Level (\d+):/);
            const xpMatch = output.match(/Total XP: ([\d,]+)/);
            const nextLevelMatch = output.match(/Next Level: ([\d,]+) XP/);

            if (levelMatch && xpMatch) {
                return {
                    level: parseInt(levelMatch[1]),
                    xp: parseInt(xpMatch[1].replace(/,/g, '')),
                    nextLevel: nextLevelMatch ? parseInt(nextLevelMatch[1].replace(/,/g, '')) : 0
                };
            }

            return null;
        } catch (error) {
            console.error('Failed to get XP status:', error);
            return null;
        }
    }

    /**
     * Get current streak
     */
    async getStreak(): Promise<number> {
        try {
            const output = await this.executeCommand([]);
            // Parse streak from output
            // Example: "🔥 Current streak: 36 days"

            const streakMatch = output.match(/streak: (\d+) day/i);
            if (streakMatch) {
                return parseInt(streakMatch[1]);
            }

            return 0;
        } catch (error) {
            console.error('Failed to get streak:', error);
            return 0;
        }
    }

    /**
     * Get today's commits
     */
    async getTodayCommits(): Promise<number> {
        try {
            const output = await this.executeCommand([]);
            // Parse commits from output
            // Example: "⚡ 2 commits today"

            const commitsMatch = output.match(/(\d+) commits? today/i);
            if (commitsMatch) {
                return parseInt(commitsMatch[1]);
            }

            return 0;
        } catch (error) {
            console.error('Failed to get today commits:', error);
            return 0;
        }
    }

    /**
     * Get dashboard stats
     */
    async getDashboardStats(): Promise<{
        commits: number;
        streak: number;
        xp: { level: number; xp: number; nextLevel: number } | null;
        topRepo: string;
    }> {
        try {
            const output = await this.executeCommand(['--dashboard']);

            // Parse dashboard output
            const commitsMatch = output.match(/Commits Today: (\d+)/);
            const streakMatch = output.match(/Streak: (\d+) day/i);
            const levelMatch = output.match(/Level (\d+):/);
            const xpMatch = output.match(/(\d+)\/(\d+) XP/);
            const repoMatch = output.match(/Top Repo: ([^\n]+)/);

            return {
                commits: commitsMatch ? parseInt(commitsMatch[1]) : 0,
                streak: streakMatch ? parseInt(streakMatch[1]) : 0,
                xp: (levelMatch && xpMatch) ? {
                    level: parseInt(levelMatch[1]),
                    xp: parseInt(xpMatch[1]),
                    nextLevel: parseInt(xpMatch[2])
                } : null,
                topRepo: repoMatch ? repoMatch[1].trim() : ''
            };
        } catch (error) {
            console.error('Failed to get dashboard stats:', error);
            return {
                commits: 0,
                streak: 0,
                xp: null,
                topRepo: ''
            };
        }
    }

    /**
     * Add TIL entry
     */
    async addTIL(content: string, template?: string): Promise<boolean> {
        try {
            const args = ['til', content];
            if (template) {
                args.push('--template', template);
            }

            await this.executeCommand(args);
            return true;
        } catch (error) {
            console.error('Failed to add TIL:', error);
            return false;
        }
    }

    /**
     * Search TIL vault
     */
    async searchTIL(query: string): Promise<string> {
        try {
            const output = await this.executeCommand(['--search-til', query]);
            return output;
        } catch (error) {
            console.error('Failed to search TIL:', error);
            return '';
        }
    }

    /**
     * Get achievements
     */
    async getAchievements(): Promise<string> {
        try {
            const output = await this.executeCommand(['--achievements']);
            return output;
        } catch (error) {
            console.error('Failed to get achievements:', error);
            return '';
        }
    }

    /**
     * Get commit message coaching
     */
    async getCoaching(message: string): Promise<string[]> {
        try {
            const output = await this.executeCommand(['--coach', message]);

            // Parse suggestions from output
            const suggestions: string[] = [];
            const lines = output.split('\n');
            let inSuggestions = false;

            for (const line of lines) {
                if (line.includes('💡 Suggestions:')) {
                    inSuggestions = true;
                    continue;
                }

                if (inSuggestions && line.trim().startsWith('💡')) {
                    suggestions.push(line.trim());
                }
            }

            return suggestions;
        } catch (error) {
            console.error('Failed to get coaching:', error);
            return [];
        }
    }

    /**
     * Check if commit-checker is installed and accessible
     */
    async checkInstallation(): Promise<boolean> {
        try {
            await this.executeCommand(['--version']);
            return true;
        } catch (error) {
            return false;
        }
    }

    /**
     * Get GitHub username from commit-checker config
     */
    async getGitHubUsername(): Promise<string> {
        try {
            // commit-checker reads from git config, so we can do the same
            const { stdout } = await execPromise('git config user.name');
            return stdout.trim();
        } catch (error) {
            console.error('Failed to get GitHub username:', error);
            return '';
        }
    }
}
