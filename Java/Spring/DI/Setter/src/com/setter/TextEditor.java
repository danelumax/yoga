package com.setter;

public class TextEditor {
	private SpellChecker spellChecker;
	private String testName;
	private int lines;
	
	public void setSpellChecker(SpellChecker spellChecker) {
		System.out.println("Inside setSpellChecker");
		this.spellChecker = spellChecker;
	}
	public void setTestName(String testName) {
		this.testName = testName;
	}
	public SpellChecker getSpellChecker() {
		return this.spellChecker;
	}
	public String getTestName() {
		return this.testName;
	}
	public void setLines(int lines) {
		this.lines = lines;
	}
	public int getLines() {
		return this.lines;
	}
	public void spellCheck() {
		this.spellChecker.checkSpelling();
		System.out.println("Test Name = " + " " + this.testName);
		System.out.println("Totol lines = " + " " + this.lines);
	}
}
