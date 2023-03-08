package analyze;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.LowerCaseFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.Tokenizer;
import org.apache.lucene.analysis.classic.ClassicTokenizer;
import org.apache.lucene.analysis.en.EnglishPossessiveFilter;
import org.apache.lucene.analysis.miscellaneous.LengthFilter;

import java.io.IOException;

import static analyze.AnalyzerUtil.consumeTokenStream;

/**
 * Analyzer for document processing, it performs tokenization and other document processing techinques
 *
 * @author Manuel Barusco (manuel.barusco@studenti.unipd.it)
 * @version 1.0
 * @since 1.0
 */
public class ToucheAnalyzer extends Analyzer {

    /**
     * default constructor
     * it creates a new instance of the ToucheAnalyzer
     */
    public ToucheAnalyzer() {
        super();
    }

    @Override
    protected TokenStreamComponents createComponents(String fieldName) {
        final Tokenizer source = new ClassicTokenizer();
        //final Tokenizer source = new LetterTokenizer();

        TokenStream tokens = new LowerCaseFilter(source);
        tokens = new EnglishPossessiveFilter(tokens);
        tokens = new LengthFilter(tokens, 3, 20);
        
        /*tokens = new StopFilter(tokens, loadStopList("smart.txt"));
        tokens = new EnglishMinimalStemFilter(tokens);
        tokens = new PorterStemFilter(tokens);
        tokens = new KStemFilter(tokens);
        tokens = new NGramTokenFilter(tokens, 3);
        tokens = new ShingleFilter(tokens, 2);*/

        return new TokenStreamComponents(source, tokens);
    }
}