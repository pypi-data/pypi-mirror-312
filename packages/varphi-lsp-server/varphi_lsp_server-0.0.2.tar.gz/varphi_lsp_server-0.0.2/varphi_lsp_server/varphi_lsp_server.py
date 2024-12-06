import sys
import logging
from datetime import datetime

from lsprotocol import types
from pygls.cli import start_server
from pygls.lsp.server import LanguageServer
from antlr4 import ParseTreeWalker, InputStream, CommonTokenStream
from varphi_parsing_tools import *
from varphi_types import *

server = LanguageServer("varphi-language-server", "v1")

def getRepresentor(program: str) -> VarphiRepresentor:
    input_stream = InputStream(program)
    lexer = VarphiLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(VarphiSyntaxErrorListener(program))
    token_stream = CommonTokenStream(lexer)
    parser = VarphiParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(VarphiSyntaxErrorListener(program))
    tree = parser.program()
    representor = VarphiRepresentor()
    walker = ParseTreeWalker()
    walker.walk(representor, tree)
    return representor

@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: LanguageServer, params: types.DidOpenTextDocumentParams):
    document_uri = params.text_document.uri
    program = ls.workspace.get_text_document(document_uri).source
    ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[]
            )
        )
    try:
        representor = getRepresentor(program)
    except VarphiSyntaxError as e:
        diagnostic = types.Diagnostic(message=str(e), severity=types.DiagnosticSeverity.Error, range=types.Range(start=types.Position(line=e.line - 1, character=e.column), end=types.Position(line=e.line - 1, character=e.column)))
        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[diagnostic]
            )
        )
        return None


@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: LanguageServer, params: types.DidOpenTextDocumentParams):
    document_uri = params.text_document.uri
    program = ls.workspace.get_text_document(document_uri).source
    ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[]
            )
        )
    try:
        representor = getRepresentor(program)
    except VarphiSyntaxError as e:
        diagnostic = types.Diagnostic(message=str(e), severity=types.DiagnosticSeverity.Error, range=types.Range(start=types.Position(line=e.line - 1, character=e.column), end=types.Position(line=e.line - 1, character=e.column)))
        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[diagnostic]
            )
        )
        return None

@server.feature(types.TEXT_DOCUMENT_HOVER)
def hover(ls: LanguageServer, params: types.HoverParams):
    pos = params.position
    document_uri = params.text_document.uri
    program = ls.workspace.get_text_document(document_uri).source
    ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[]
            )
        )
    try:
        representor = getRepresentor(program)
    except VarphiSyntaxError as e:
        diagnostic = types.Diagnostic(message=str(e), severity=types.DiagnosticSeverity.Error, range=types.Range(start=types.Position(line=e.line - 1, character=e.column), end=types.Position(line=e.line - 1, character=e.column)))
        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[diagnostic]
            )
        )
        return None

    elementAtCursor = representor.positionToObject[(pos.line + 1, pos.character)]

    if isinstance(elementAtCursor, State):
        hoverContent = "Deterministic " if len(elementAtCursor.onTally) <= 1 and len(elementAtCursor.onBlank) <= 1 else "Non-Deterministic "
        hoverContent += f"State `{elementAtCursor.name}`\n\n\n"
        return types.Hover(
            contents=types.MarkupContent(
                kind=types.MarkupKind.Markdown,
                value=hoverContent
            ),
            range=types.Range(
                start=types.Position(line=pos.line, character=pos.character),
                end=types.Position(line=pos.line, character=pos.character),
            ),
        )


@server.feature(types.TEXT_DOCUMENT_REFERENCES)
def references(ls: LanguageServer, params: types.HoverParams):
    pos = params.position
    document_uri = params.text_document.uri
    program = ls.workspace.get_text_document(document_uri).source
    ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[]
            )
        )
    try:
        representor = getRepresentor(program)
    except VarphiSyntaxError as e:
        diagnostic = types.Diagnostic(message=str(e), severity=types.DiagnosticSeverity.Error, range=types.Range(start=types.Position(line=e.line - 1, character=e.column), end=types.Position(line=e.line - 1, character=e.column)))
        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[diagnostic]
            )
        )
        return None

    elementAtCursor = representor.positionToObject[(pos.line + 1, pos.character)]

    

    if isinstance(elementAtCursor, State):
        references = []
        for reference in elementAtCursor.references:
            startPosition = types.Position(reference[0] - 1, reference[1][0])
            endPosition = types.Position(reference[0] - 1, reference[1][1] + 1)
            references.append(types.Location(uri=document_uri, range=types.Range(start=startPosition, end=endPosition)))
        return references
    
    return None

@server.feature(types.TEXT_DOCUMENT_IMPLEMENTATION)
@server.feature(types.TEXT_DOCUMENT_DECLARATION)
@server.feature(types.TEXT_DOCUMENT_DEFINITION)
def implementations(ls: LanguageServer, params: types.HoverParams):
    pos = params.position
    document_uri = params.text_document.uri
    program = ls.workspace.get_text_document(document_uri).source
    ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[]
            )
        )
    try:
        representor = getRepresentor(program)
    except VarphiSyntaxError as e:
        diagnostic = types.Diagnostic(message=str(e), severity=types.DiagnosticSeverity.Error, range=types.Range(start=types.Position(line=e.line - 1, character=e.column), end=types.Position(line=e.line - 1, character=e.column)))
        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[diagnostic]
            )
        )
        return None

    elementAtCursor = representor.positionToObject[(pos.line + 1, pos.character)]

    

    if isinstance(elementAtCursor, State):
        references = []
        for reference in elementAtCursor.implementations:
            startPosition = types.Position(reference[0] - 1, reference[1][0])
            endPosition = types.Position(reference[0] - 1, reference[1][1] + 1)
            references.append(types.Location(uri=document_uri, range=types.Range(start=startPosition, end=endPosition)))
        return references
    
    return None


@server.feature(
    types.TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
    types.SemanticTokensLegend(
        token_types=["state", "initialState", "tapeCharacter", "headDirection", "comment"],
        token_modifiers=[],
    ),
)
def semantic_tokens_full(ls: LanguageServer, params: types.SemanticTokensParams):
    """Return the semantic tokens for the entire document"""
    document_uri = params.text_document.uri
    program = ls.workspace.get_text_document(document_uri).source
    ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[]
            )
        )
    try:
        representor = getRepresentor(program)
    except VarphiSyntaxError as e:
        diagnostic = types.Diagnostic(message=str(e), severity=types.DiagnosticSeverity.Error, range=types.Range(start=types.Position(line=e.line - 1, character=e.column), end=types.Position(line=e.line - 1, character=e.column)))
        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[diagnostic]
            )
        )
        return None
    data = []
    previousLine = 0
    previousColumn = 0
    for positionRange in representor.positionRangeToObject:
        line = positionRange[0][0] - 1
        startColumn = positionRange[0][1]
        endColumn = positionRange[1][1]
        
        length = endColumn - startColumn + 1

        relativeLine = line - previousLine
        if relativeLine == 0:
            relativeColumn = startColumn - previousColumn
        else:
            relativeColumn = 0
        previousLine = line
        previousColumn = startColumn
        element = representor.positionRangeToObject[positionRange]
        if isinstance(element, State):
            if element is representor.initialState:
                tokenTypeIndex = 1
            else:
                tokenTypeIndex = 0
        elif isinstance(element, TapeCharacter):
            tokenTypeIndex = 2
        elif isinstance(element, HeadDirection):
            tokenTypeIndex = 3
        elif isinstance(element, Comment):
            tokenTypeIndex = 4
        tokenModifiers = 0
        data.extend([relativeLine, relativeColumn, length, tokenTypeIndex, tokenModifiers])
    return types.SemanticTokens(data=data)


@server.feature(types.TEXT_DOCUMENT_RENAME)
def rename(ls: LanguageServer, params: types.RenameParams):
    """Rename the symbol at the given position."""
    document_uri = params.text_document.uri
    program = ls.workspace.get_text_document(document_uri).source
    ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[]
            )
        )
    try:
        representor = getRepresentor(program)
    except VarphiSyntaxError as e:
        diagnostic = types.Diagnostic(message=str(e), severity=types.DiagnosticSeverity.Error, range=types.Range(start=types.Position(line=e.line - 1, character=e.column), end=types.Position(line=e.line - 1, character=e.column)))
        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=document_uri,
                version=ls.workspace.get_text_document(document_uri).version,
                diagnostics=[diagnostic]
            )
        )
        return None
    line = params.position.line + 1
    column = params.position.character
    element = representor.positionToObject[line, column]
    edits = []
    if isinstance(element, State):
        references = element.references
        for reference in references:
            edits.append(
                types.TextEdit(
                    new_text=params.new_name,
                    range=types.Range(
                        start=types.Position(line=reference[0] - 1, character=reference[1][0]),
                        end=types.Position(line=reference[0] - 1, character=reference[1][1] + 1),
                    ),
                )
            )
    return types.WorkspaceEdit(changes={params.text_document.uri: edits})

def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    start_server(server)

if __name__ == "__main__":
    main()