
package compress;

import java.awt.BorderLayout;
import java.awt.Dimension;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.border.TitledBorder;
import com.module.core.Module;
import com.module.core.ModuleDesc;
import com.module.ModuleInChain;
import com.module.core.Trace;

@SuppressWarnings("serial")
@ModuleDesc(pkgName="Resample", name="WindowedResample", desc="",isVisible=false)
public class WindowedResample extends Module implements ModuleInChain {

    public static final String COMPRESS_RATIO = "compress.ratio";
    public static final String OVERLAP_RATIO = "overlap.ratio";
    
    private static final int MIN_COMPRESS_RATIO = 1;
    
    private static final float MIN_OVERLAP_RATIO = 0.0f;
    private static final float MAX_OVERLAP_RATIO = 1f;
    private static final float DEFAULT_OVERLAP_RATIO = 0.5f;

    protected JTextField compressRatioTextField;
    protected JTextField overlapRatioTextField;
    protected float overlapRatio;
    protected int compressRatio;
    protected float scale;

    /** method to initialize the module */
    @Override
    public void initModule() {
        moduleTitle = "WindowedResample";
        prefix = "WinRes";
        moduleDescription = "Compress traces with fixed window size";
        moduleVersion = "1.1";
        helpFile = "doc/manual/modulesWindowedResample.html";
        compressRatio = 1;
        overlapRatio = 0;
        set(COMPRESS_RATIO, compressRatio);
        set(OVERLAP_RATIO, overlapRatio);
    }

    @Override
    public JPanel initDialog() {
        JPanel parameterPanel = new JPanel(new java.awt.GridLayout(1, 2));
        JPanel compressRatioPanel = new JPanel(new BorderLayout());
        compressRatioPanel.setBorder(new TitledBorder("Window size"));
        compressRatioTextField = new JTextField(String.valueOf(compressRatio));
        compressRatioTextField.setPreferredSize(new Dimension(50, 20));
        compressRatioTextField.setToolTipText("Compress ratio (Number of input samples to join per compressed sample)");
        compressRatioPanel.add(compressRatioTextField, BorderLayout.CENTER);
        parameterPanel.add(compressRatioPanel);
        JPanel overlapRatioPanel = new JPanel(new BorderLayout());
        overlapRatioPanel.setBorder(new TitledBorder("Overlap ratio"));
        overlapRatioTextField = new JTextField(String.valueOf(overlapRatio));
        overlapRatioTextField.setPreferredSize(new Dimension(50, 20));
        overlapRatioTextField.setToolTipText("Fraction overlap between compressed samples (0 >= overlap < 1)");
        overlapRatioPanel.add(overlapRatioTextField, BorderLayout.CENTER);
        parameterPanel.add(overlapRatioPanel);
        return parameterPanel;
    }

    @Override
    public void setDialogValues() {
        setInt(compressRatioTextField, COMPRESS_RATIO);
        setFloat(overlapRatioTextField, OVERLAP_RATIO, 3);
    }

    @Override
    public void getDialogValues() {
        compressRatio = parseInt(compressRatioTextField, COMPRESS_RATIO, 1, 10);
        overlapRatio = parseFloat(overlapRatioTextField, OVERLAP_RATIO);
        if (compressRatio < MIN_COMPRESS_RATIO) {
            System.err.println("Compress ratio less than minimum, resetting to: "+MIN_COMPRESS_RATIO);
            compressRatio = MIN_COMPRESS_RATIO;
        }
        if (overlapRatio < MIN_OVERLAP_RATIO || overlapRatio >= MAX_OVERLAP_RATIO) {
            System.err.println("Overlap ratio not within 0..1 range, resetting to: "+DEFAULT_OVERLAP_RATIO);
            overlapRatio = DEFAULT_OVERLAP_RATIO;
        }
        scale = compressRatio * (1 - overlapRatio);
    }

    /**
     * Method for processing a single trace
     * 
     * @param t Trace to process
     * @return resulting Trace
     */
    @Override
    public Trace process(Trace t) {
        float[] sample = t.getSample();
        int len = (int) StrictMath.ceil(sample.length / scale);
        float[] s = new float[len];
        for (int i = 0; i < len; i++) {
            double d = 0;
            int floor = (int) (i * scale);
            for (int j = 0, k = floor; j < compressRatio & k < sample.length; j++, k++) { // compress multiple samples into one
                boolean first = j == 0;
                if (first) { // first, must be weighed less, if outside section
                    d += sample[k] * (k + 1 - (i * scale));
                } else { // not first
                    d += sample[k];
                }
            }
            if ((i * scale) - floor > 0 & floor + compressRatio < numberOfSamples) { // i*scale not an integer value, and more points available
                d += sample[floor + compressRatio] * ((i * scale) - floor);
            }
            s[i] = (float) (d / compressRatio);
        }
        return new Trace(t.getTitle(), t.getData(), s, (t.getSampleFrequency() * len) / sample.length);
    }

}
