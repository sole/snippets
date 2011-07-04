Command line + GUI (GTK based) Android ADB-based file explorer

If you don't want to be specifying the path to adb all the time, just add the path that contains its executable to your $PATH environment variable.
For example, edit .bashrc and add it like this:

	PATH=$PATH:~/Applications/android-sdk-linux_86/platform-tools

The line above appends adb's path to whatever value $PATH held before. The path might be different, according to wherever you've installed the Android SDK.

Attributions

Using FamFamFam icons
