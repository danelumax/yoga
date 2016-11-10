package com.constructor;

public class TextEditor {
	private SpellChecker spellChecker;
	private String testName;
	private int lines;
	
	public TextEditor(SpellChecker spellChecker, String testName, int lines) {
		System.out.println("Inside TextEditor constructor");
		this.spellChecker = spellChecker;
		this.testName = testName;
		this.lines = lines;
	}
	public void spellCheck() {
		this.spellChecker.checkSpelling();
		System.out.println("Test Name = " + " " + this.testName);
		System.out.println("Totol lines = " + " " + this.lines);
	}
}
