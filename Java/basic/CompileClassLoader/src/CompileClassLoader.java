import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.lang.reflect.Method;

public class CompileClassLoader extends ClassLoader{
	private byte[] getBytes(String filename)
		throws IOException {
		File file = new File(filename);
		long len = file.length();
		byte[] raw = new byte[(int)len];
		try(
			FileInputStream fin = new FileInputStream(file)) {
			int r = fin.read(raw);
			if (r != len) {
				throw new IOException("Can not read total file: " + r + " != " + len);
			}
			return raw;
		}
	}
	
	private boolean compile(String javaFile)
		throws IOException {
		System.out.println("CompileClassLoader: Compiling " + javaFile + " ...");
		Process p = Runtime.getRuntime().exec("javac " + javaFile);
		try {
			p.waitFor();
		}
		catch(InterruptedException ie) {
			System.out.println(ie);
		}
		
		int ret = p.exitValue();
		return ret == 0;
	}
	
	protected Class<?> findClass(String name)
		throws ClassNotFoundException {
		Class clazz = null;
		String fileStub = name.replace(".", "/");
		String javaFilename = fileStub + ".java";
		String classFilename = fileStub + ".class";
		File javaFile = new File(javaFilename);
		File classFile = new File(classFilename);
		
		if (javaFile.exists() && (!classFile.exists()
			|| javaFile.lastModified() > classFile.lastModified())) {
			try {
				if (!compile(javaFilename) || !classFile.exists()) {
					if (!compile(javaFilename) || !classFile.exists()) {
						throw new ClassNotFoundException("ClassNotFoundException: " + javaFilename);
					}
				}
			}
			catch (IOException ex) {
				ex.printStackTrace();
			}
		}
		
		if (classFile.exists()) {
			try {
				byte[] raw = getBytes(classFilename);
				clazz = defineClass(name, raw, 0, raw.length);
			}
			catch (IOException ie)
			{
				ie.printStackTrace();
			}
		}
		
		if (clazz == null) {
			throw new ClassNotFoundException(name);
		}
		
		return clazz;
	}
	
	public static void main(String[] args) throws Exception {
		if (args.length < 1) {
			System.out.println("Missing Object Class, please follow the blew way to run Java file");
			System.out.println("java CompileClassLoader ClassName");
			throw new IOException("throw Error");
		}
		String progClass = args[0];
		String[] progArgs = new String[args.length-1];
		System.arraycopy(args, 1, progArgs, 0, progArgs.length);
		CompileClassLoader ccl = new CompileClassLoader();
		Class<?> clazz = ccl.loadClass(progClass);
		
		Method main = clazz.getMethod("main", (new String[0].getClass()));
		Object argsArray[] = {progArgs};
		main.invoke(null, argsArray);
	}
}
