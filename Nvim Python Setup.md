# Python Debugger Setup Guide for Neovim

Complete guide to set up Python development environment with debugging capabilities in Neovim using NvChad.

## Prerequisites

- Ubuntu/Debian-based system (WSL supported)
- Git installed
- Python 3 installed

## Step 1: Install Neovim

### Install Neovim (Latest Version)
```bash
# Remove old version if exists
sudo apt remove neovim

# Install latest Neovim
curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.linux64.tar.gz
sudo rm -rf /opt/nvim
sudo tar -C /opt -xzf nvim.linux64.tar.gz
sudo ln -sf /opt/nvim-linux64/bin/nvim /usr/local/bin/nvim

# Verify installation
nvim --version
```

### Install NvChad
```bash
# Backup existing config (if any)
mv ~/.config/nvim ~/.config/nvim.backup

# Install NvChad
git clone https://github.com/NvChad/starter ~/.config/nvim
```

## Step 2: Install Mason and Language Server

### First Launch and Basic Setup
```bash
# Launch Neovim
nvim

# In Neovim, install Mason
:MasonInstall
```

### Install Python Language Server and Debugger
```bash
# Open Mason interface
:Mason

# Navigate and install:
# - python-lsp-server (or pyright)
# - debugpy
# - ruff (optional: Python linter)
```

Or install via command:
```vim
:MasonInstall python-lsp-server debugpy ruff
```

## Step 3: Configure LSP for Python

### Edit LSP Configuration
Create/edit `~/.config/nvim/lua/configs/lspconfig.lua`:

```lua
require("nvchad.configs.lspconfig").defaults()

-- Python LSP
require'lspconfig'.pyright.setup{}

-- Add other servers as needed
local servers = { "html", "cssls" }
vim.lsp.enable(servers)
```

## Step 4: Set Up Python Debugger

### Add DAP Plugins
Create/edit `~/.config/nvim/lua/plugins/init.lua`:

```lua
return {
  {
    "stevearc/conform.nvim",
    opts = require "configs.conform",
  },
  {
    "neovim/nvim-lspconfig",
    config = function()
      require "configs.lspconfig"
    end,
  },
  
  -- Debug Adapter Protocol
  {
    "mfussenegger/nvim-dap",
    config = function()
      local dap = require("dap")
      
      -- Python debugpy configuration
      dap.adapters.python = {
        type = 'executable',
        command = vim.fn.stdpath("data") .. '/mason/packages/debugpy/venv/bin/python',
        args = { '-m', 'debugpy.adapter' },
      }

      dap.configurations.python = {
        {
          type = 'python',
          request = 'launch',
          name = "Launch file",
          program = "${file}",
          pythonPath = function()
            return '/usr/bin/python3'
          end,
        },
      }
    end
  },
  
  -- Required dependency for nvim-dap-ui
  {
    "nvim-neotest/nvim-nio"
  },
  
  -- DAP UI
  {
    "rcarriga/nvim-dap-ui",
    dependencies = {"mfussenegger/nvim-dap", "nvim-neotest/nvim-nio"},
    config = function()
      local dap, dapui = require("dap"), require("dapui")
      dapui.setup()
      
      dap.listeners.after.event_initialized["dapui_config"] = function()
        dapui.open()
      end
      dap.listeners.before.event_terminated["dapui_config"] = function()
        dapui.close()
      end
      dap.listeners.before.event_exited["dapui_config"] = function()
        dapui.close()
      end
    end
  },
  
  -- Virtual text showing variable values
  {
    "theHamsta/nvim-dap-virtual-text",
    dependencies = {"mfussenegger/nvim-dap"},
    config = function()
      require("nvim-dap-virtual-text").setup()
    end
  }
}
```

### Add Debug Keybindings
Add to `~/.config/nvim/init.lua`:

```lua
-- DAP keybindings using Lua functions
vim.keymap.set("n", "<leader>db", function() require('dap').toggle_breakpoint() end, { desc = "Toggle Breakpoint" })
vim.keymap.set("n", "<leader>dc", function() require('dap').continue() end, { desc = "Start/Continue Debug" })
vim.keymap.set("n", "<leader>ds", function() require('dap').step_over() end, { desc = "Step Over" })
vim.keymap.set("n", "<leader>di", function() require('dap').step_into() end, { desc = "Step Into" })
vim.keymap.set("n", "<leader>do", function() require('dap').step_out() end, { desc = "Step Out" })
vim.keymap.set("n", "<leader>dt", function() require('dap').terminate() end, { desc = "Terminate Debug" })
vim.keymap.set("n", "<leader>du", function() require('dapui').toggle() end, { desc = "Toggle Debug UI" })
```

## Step 5: Test the Setup

### Install Plugins
```bash
# Restart Neovim and sync plugins
nvim
:Lazy sync
```

### Create Test Python File
Create `test.py`:

```python
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

def main():
    numbers = [3, 4, 5]
    
    for num in numbers:
        result = factorial(num)  # Set breakpoint here
        print(f"Factorial of {num} is {result}")

if __name__ == "__main__":
    main()
```

### Debug Workflow

1. **Open the file**: `nvim test.py`
2. **Set breakpoint**: Move cursor to line 9, press `<leader>db`
3. **Start debugging**: Press `<leader>dc`
4. **Use debug controls**:
   - `<leader>ds` - Step over
   - `<leader>di` - Step into function
   - `<leader>do` - Step out
   - `<leader>du` - Toggle debug UI
   - `<leader>dt` - Terminate debugging

## Debug Keybindings Reference

| Keybinding | Action |
|------------|--------|
| `<leader>db` | Toggle Breakpoint |
| `<leader>dc` | Start/Continue Debug |
| `<leader>ds` | Step Over |
| `<leader>di` | Step Into |
| `<leader>do` | Step Out |
| `<leader>dt` | Terminate Debug |
| `<leader>du` | Toggle Debug UI |

*Note: `<leader>` is typically the Space key in NvChad*

## Verification Commands

### Check LSP Status
```vim
:LspInfo
```

### Check DAP Status
```vim
:lua print(vim.inspect(require('dap')))
```

### Check Installed Packages
```vim
:Mason
```

## Troubleshooting

### Common Issues

**LSP not working:**
- Ensure `pyright` or `python-lsp-server` is installed via Mason
- Check `:LspInfo` for active clients

**Debugger not starting:**
- Verify `debugpy` is installed: `:Mason`
- Check debugpy path: `ls ~/.local/share/nvim/mason/packages/debugpy/venv/bin/`

**Keybindings not working:**
- Restart Neovim after configuration changes
- Test with Lua command: `:lua require('dap').toggle_breakpoint()`

### File Structure
Your final configuration should look like:
```
~/.config/nvim/
├── init.lua
├── lua/
│   ├── chadrc.lua
│   ├── configs/
│   │   └── lspconfig.lua
│   └── plugins/
│       └── init.lua
```

## Additional Features

### Optional: Auto-format on Save
Add to `~/.config/nvim/lua/configs/conform.lua`:
```lua
return {
  formatters_by_ft = {
    python = { "black" },
  },
  format_on_save = {
    timeout_ms = 500,
    lsp_fallback = true,
  },
}
```

Install formatter:
```vim
:MasonInstall black
```

---

**Congratulations!** You now have a fully functional Python development environment with debugging capabilities in Neovim. Happy coding! 🐍✨