---
title: Ghostty - A Fast and Feature-Rich Terminal Emulator
description: Ghostty is a fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration.
created: 2026-07-03
tags:
  - terminal
  - emulator
  - productivity
  - command-line
  - cross-platform
status: draft
---

# Ghostty - A Fast and Feature-Rich Terminal Emulator

Ghostty is a fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration. It is designed to be the best drop-in replacement for your current terminal emulator on macOS and Linux. Ghostty was developed by Mitchell Hashimoto, a co-founder of HashiCorp, and it aims to be the new performance standard in 2026.

## What is Ghostty?

Ghostty is not a tool for generating projects or scaffolding applications, but rather a terminal emulator that provides a modern and efficient user interface. It offers a fast and responsive experience, with GPU acceleration and a native UI, making it a superior choice for developers looking to boost their productivity in a terminal environment.

## Key Features

- **Platform-Native UI**: Provides a modern and intuitive user interface.
- **GPU Acceleration**: Enhances performance and responsiveness.
- **Cross-Platform Support**: Works seamlessly on macOS, Linux, and Windows.
- **Fast**: Offers lightning-fast performance, even with complex commands and large file operations.
- **Feature-Rich**: Includes advanced features such as tabbed terminals, multiple panes, and more.

## History

Ghostty was created by the Ghost Project team, which aims to simplify the process of building content management systems and web applications. Mitchell Hashimoto, a former CEO and CTO of HashiCorp, is the lead developer of Ghostty and is dedicated to enhancing the terminal emulator experience.

## Use Cases

Ghostty is primarily used in a terminal environment for interacting with command-line tools, managing processes, and executing scripts. It is particularly useful for developers and system administrators who need a fast and efficient terminal emulator.

## Installation

To install Ghostty, follow these steps:

1. **Install Node.js**: Ensure you have Node.js installed on your system. Ghostty is built using Node.js.
2. **Install Ghostty**: Open your terminal and run the following command:

   ```sh
   npm install -g ghostty
   ```

   Alternatively, you can install it via Yarn:

   ```sh
   yarn global add ghostty
   ```

## Basic Usage

Once installed, you can use Ghostty to interact with your terminal. Here are some basic commands:

1. **Start Ghostty**: Open Ghostty by simply running the command:

   ```sh
   ghostty
   ```

2. **Open a New Terminal**: You can open a new terminal window within Ghostty:

   ```sh
   ghostty new-terminal
   ```

3. **Close the Current Terminal**: Exit the current terminal window:

   ```sh
   ghostty close-terminal
   ```

4. **Switch Between Terminals**: Use the tab key to switch between open terminals:

   ```sh
   ghostty switch-terminal
   ```

5. **Open a File**: Open a file in the terminal:

   ```sh
   ghostty open-file /path/to/file.txt
   ```

6. **Run a Command in the Terminal**: Execute a command in the terminal:

   ```sh
   ghostty run-command ls -l
   ```

7. **Close Ghostty**: Exit Ghostty by pressing `Ctrl + D` or running:

   ```sh
   ghostty exit
   ```

## Conclusion

Ghostty is a powerful and efficient terminal emulator that offers a modern and responsive user interface. It is designed to enhance your productivity in a terminal environment and is a worthy choice for developers and system administrators looking for a fast and feature-rich terminal emulator.

For more information and to explore additional features, visit the [official Ghostty GitHub repository](https://github.com/mitchellh/ghostty).