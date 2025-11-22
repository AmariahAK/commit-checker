import * as vscode from 'vscode';
import { CommitCheckerIntegration } from './commitChecker';

let statusBarItem: vscode.StatusBarItem;
let commitChecker: CommitCheckerIntegration;
let refreshInterval: NodeJS.Timeout | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('Commit Checker extension is now active');

    // Initialize commit-checker integration
    commitChecker = new CommitCheckerIntegration();

    // Check if commit-checker is installed
    checkInstallation();

    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    statusBarItem.command = 'commit-checker.showDashboard';
    context.subscriptions.push(statusBarItem);

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('commit-checker.showDashboard', showDashboard),
        vscode.commands.registerCommand('commit-checker.refreshStats', refreshStats),
        vscode.commands.registerCommand('commit-checker.addTIL', addTIL),
        vscode.commands.registerCommand('commit-checker.searchTIL', searchTIL),
        vscode.commands.registerCommand('commit-checker.viewAchievements', viewAchievements)
    );

    // Initial stats update
    updateStatusBar();

    // Set up auto-refresh
    setupAutoRefresh();
}

async function checkInstallation() {
    const installed = await commitChecker.checkInstallation();

    if (!installed) {
        vscode.window.showWarningMessage(
            'commit-checker CLI not found. Please install it to use this extension.',
            'View Instructions'
        ).then(selection => {
            if (selection === 'View Instructions') {
                vscode.env.openExternal(vscode.Uri.parse('https://github.com/AmariahAK/commit-checker#-quick-install-recommended'));
            }
        });
    }
}

async function updateStatusBar() {
    try {
        const config = vscode.workspace.getConfiguration('commit-checker');
        const showStatusBar = config.get('showStatusBar', true);

        if (!showStatusBar) {
            statusBarItem.hide();
            return;
        }

        const [streak, commits, xpStatus] = await Promise.all([
            commitChecker.getStreak(),
            commitChecker.getTodayCommits(),
            commitChecker.getXPStatus()
        ]);

        const streakIcon = streak > 0 ? '🔥' : '📊';
        const level = xpStatus ? `Lv${xpStatus.level}` : '';

        statusBarItem.text = `${streakIcon} ${streak}d | ${commits} commits | ${level}`;
        statusBarItem.tooltip = `Streak: ${streak} days\\nCommits today: ${commits}\\n${xpStatus ? `Level ${xpStatus.level} - ${xpStatus.xp} XP` : ''}\\n\\nClick to open dashboard`;
        statusBarItem.show();
    } catch (error) {
        console.error('Failed to update status bar:', error);
        statusBarItem.text = '$(question) Commit Checker';
        statusBarItem.tooltip = 'Failed to load stats. Click to retry.';
        statusBarItem.show();
    }
}

function setupAutoRefresh() {
    const config = vscode.workspace.getConfiguration('commit-checker');
    const intervalSeconds = config.get('refreshInterval', 300); // Default: 5 minutes

    if (refreshInterval) {
        clearInterval(refreshInterval);
    }

    refreshInterval = setInterval(() => {
        updateStatusBar();
    }, intervalSeconds * 1000);
}

async function showDashboard() {
    try {
        const stats = await commitChecker.getDashboardStats();

        const panel = vscode.window.createWebviewPanel(
            'commitCheckerDashboard',
            'Commit Checker Dashboard',
            vscode.ViewColumn.One,
            { enableScripts: true }
        );

        panel.webview.html = getDashboardHTML(stats);
    } catch (error) {
        vscode.window.showErrorMessage(`Failed to load dashboard: ${error}`);
    }
}

function getDashboardHTML(stats: any): string {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline';">
    <style>
        body {
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
            padding: 20px;
        }
        .stat-card {
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 3px solid var(--vscode-activityBarBadge-background);
        }
        .stat-label {
            font-size: 12px;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
        }
        .progress-bar {
            width: 100%;
            height: 8px;
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }
        .progress-fill {
            height: 100%;
            background-color: var(--vscode-progressBar-background);
            transition: width 0.3s ease;
        }
        h1 {
            margin-bottom: 20px;
            border-bottom: 1px solid var(--vscode-panel-border);
            padding-bottom: 10px;
        }
    </style>
</head>
<body>
    <h1>📊 Commit Checker Dashboard</h1>
    
    <div class="stat-card">
        <div class="stat-label">COMMITS TODAY</div>
        <div class="stat-value">${stats.commits === 1 ? '🟢' : stats.commits > 1 ? '🔥' : '⚪'} ${stats.commits}</div>
    </div>

    <div class="stat-card">
        <div class="stat-label">CURRENT STREAK</div>
        <div class="stat-value">🔥 ${stats.streak} days</div>
    </div>

    ${stats.xp ? `
    <div class="stat-card">
        <div class="stat-label">LEVEL & XP</div>
        <div class="stat-value">⚡ Level ${stats.xp.level}</div>
        <div style="margin-top: 10px; font-size: 14px;">
            ${stats.xp.xp.toLocaleString()} / ${stats.xp.nextLevel.toLocaleString()} XP
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: ${(stats.xp.xp / stats.xp.nextLevel) * 100}%"></div>
        </div>
    </div>
    ` : ''}

    ${stats.topRepo ? `
    <div class="stat-card">
        <div class="stat-label">TOP REPOSITORY</div>
        <div class="stat-value">📁 ${stats.topRepo}</div>
    </div>
    ` : ''}

    <div style="margin-top: 30px; text-align: center; opacity: 0.6; font-size: 12px;">
        Run 'commit-checker' in terminal for full stats and insights
    </div>
</body>
</html>
    `;
}

async function refreshStats() {
    await updateStatusBar();
    vscode.window.showInformationMessage('Stats refreshed!');
}

async function addTIL() {
    const content = await vscode.window.showInputBox({
        prompt: 'What did you learn today?',
        placeHolder: 'e.g., Learned how to use async/await in TypeScript'
    });

    if (!content) {
        return;
    }

    const useTemplate = await vscode.window.showQuickPick(
        ['No template', 'bugfix', 'feature', 'concept', 'tool', 'algorithm'],
        { placeHolder: 'Select a template (optional)' }
    );

    const template = useTemplate && useTemplate !== 'No template' ? useTemplate : undefined;

    const success = await commitChecker.addTIL(content, template);

    if (success) {
        vscode.window.showInformationMessage(`✅ TIL entry added: "${content}"`);
    } else {
        vscode.window.showErrorMessage('Failed to add TIL entry');
    }
}

async function searchTIL() {
    const query = await vscode.window.showInputBox({
        prompt: 'Search your TIL vault',
        placeHolder: 'e.g., async, python, bug'
    });

    if (!query) {
        return;
    }

    const results = await commitChecker.searchTIL(query);

    if (results) {
        const panel = vscode.window.createWebviewPanel(
            'tilSearchResults',
            `TIL Search: ${query}`,
            vscode.ViewColumn.One,
            {}
        );

        panel.webview.html = `
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {
                        font-family: var(--vscode-font-family);
                        color: var(--vscode-foreground);
                        padding: 20px;
                    }
                    pre {
                        white-space: pre-wrap;
                        word-wrap: break-word;
                    }
                </style>
            </head>
            <body>
                <h1>TIL Search Results: "${query}"</h1>
                <pre>${results}</pre>
            </body>
            </html>
        `;
    } else {
        vscode.window.showInformationMessage('No TIL entries found');
    }
}

async function viewAchievements() {
    const achievements = await commitChecker.getAchievements();

    const panel = vscode.window.createWebviewPanel(
        'achievements',
        'Achievements',
        vscode.ViewColumn.One,
        {}
    );

    panel.webview.html = `
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: var(--vscode-font-family);
                    color: var(--vscode-foreground);
                    padding: 20px;
                }
                pre {
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }
            </style>
        </head>
        <body>
            <pre>${achievements}</pre>
        </body>
        </html>
    `;
}

export function deactivate() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
}
