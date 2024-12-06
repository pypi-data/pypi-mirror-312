from nlpx.model.classifier import TextCNNClassifier

if __name__ == '__main__':
	model = TextCNNClassifier(128, vocab_size=10, num_classes=2)
	for p in model.named_modules():
		print(p)
